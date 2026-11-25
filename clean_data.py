
from pathlib import Path
import logging
import pandas as pd


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

FAQ_INPUT = DATA_DIR / "faq_data.csv"
PRODUCT_INPUT = DATA_DIR / "ecommerce_data_final.csv"

FAQ_OUTPUT = PROCESSED_DIR / "faq_cleaned.csv"
PRODUCT_OUTPUT = PROCESSED_DIR / "products_cleaned.csv"

REQUIRED_FAQ_COLUMNS = {"question", "answer"}

REQUIRED_PRODUCT_COLUMNS = {
    "product_link",
    "title",
    "brand",
    "price",
    "discount",
    "avg_rating",
    "total_ratings",
}


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. COMMON VALIDATION FUNCTIONS
# --------------------------------------------------

def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file and validate its existence."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    try:
        return pd.read_csv(file_path)
    except Exception as exc:
        raise ValueError(
            f"Unable to read {file_path.name}: {exc}"
        ) from exc


def validate_columns(
    df: pd.DataFrame,
    required_columns: set,
    dataset_name: str
) -> None:
    """Check whether all required columns exist."""

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing columns: "
            f"{sorted(missing_columns)}"
        )


def clean_text_columns(
    df: pd.DataFrame,
    columns: list
) -> pd.DataFrame:
    """Remove leading and trailing whitespace."""

    for column in columns:
        df[column] = df[column].astype("string").str.strip()

        df[column] = df[column].replace("", pd.NA)

    return df


# --------------------------------------------------
# 4. FAQ DATA CLEANING
# --------------------------------------------------

def clean_faq_data() -> pd.DataFrame:

    logger.info("Loading FAQ dataset...")

    faq_df = load_csv(FAQ_INPUT)

    validate_columns(
        faq_df,
        REQUIRED_FAQ_COLUMNS,
        "FAQ dataset"
    )

    faq_df = faq_df[
        ["question", "answer"]
    ].copy()

    faq_df = clean_text_columns(
        faq_df,
        ["question", "answer"]
    )

    faq_df = faq_df.dropna(
        subset=["question", "answer"]
    )

    faq_df = faq_df.drop_duplicates(
        subset=["question"],
        keep="first"
    )

    if faq_df.empty:
        raise ValueError("FAQ dataset is empty after cleaning.")

    return faq_df.reset_index(drop=True)


# --------------------------------------------------
# 5. PRODUCT DATA CLEANING
# --------------------------------------------------

def clean_product_data() -> pd.DataFrame:

    logger.info("Loading product dataset...")

    product_df = load_csv(PRODUCT_INPUT)

    validate_columns(
        product_df,
        REQUIRED_PRODUCT_COLUMNS,
        "Product dataset"
    )

    product_df = product_df[
        sorted(REQUIRED_PRODUCT_COLUMNS)
    ].copy()

    # Clean text fields
    product_df = clean_text_columns(
        product_df,
        ["product_link", "title", "brand"]
    )

    # Standardize brand names
    product_df["brand"] = (
        product_df["brand"]
        .str.title()
    )

    # Preserve known brand styling
    brand_mapping = {
        "Hrx By Hrithik Roshan": "HRX by Hrithik Roshan",
        "Us Polo Assn": "U.S. Polo Assn.",
    }

    product_df["brand"] = (
        product_df["brand"]
        .replace(brand_mapping)
    )

    # Convert numeric columns safely
    numeric_columns = [
        "price",
        "discount",
        "avg_rating",
        "total_ratings",
    ]

    for column in numeric_columns:
        product_df[column] = pd.to_numeric(
            product_df[column],
            errors="coerce"
        )

    # Remove records with missing essential fields
    product_df = product_df.dropna(
        subset=[
            "product_link",
            "title",
            "brand",
            *numeric_columns,
        ]
    )

    # Validate business rules
    valid_rows = (
        (product_df["price"] > 0)
        & product_df["discount"].between(0, 1)
        & product_df["avg_rating"].between(1, 5)
        & (product_df["total_ratings"] >= 0)
        & (product_df["total_ratings"] % 1 == 0)
        & (product_df["price"] % 1 == 0)
    )

    invalid_count = (~valid_rows).sum()

    if invalid_count:
        logger.warning(
            "Removing %d products with invalid numeric values.",
            invalid_count
        )

    product_df = product_df.loc[valid_rows].copy()

    # Restore integer types
    product_df["price"] = product_df["price"].astype("int64")
    product_df["total_ratings"] = (
        product_df["total_ratings"].astype("int64")
    )

    # Remove duplicate product URLs
    product_df = product_df.drop_duplicates(
        subset=["product_link"],
        keep="first"
    )

    if product_df.empty:
        raise ValueError(
            "Product dataset is empty after cleaning."
        )

    return product_df.reset_index(drop=True)


# --------------------------------------------------
# 6. SAVE CLEANED DATASETS
# --------------------------------------------------

def save_dataset(
    df: pd.DataFrame,
    output_path: Path
) -> None:

    df.to_csv(output_path, index=False)

    logger.info(
        "Saved %d records to %s",
        len(df),
        output_path
    )


# --------------------------------------------------
# 7. MAIN EXECUTION
# --------------------------------------------------

def main():

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    faq_df = clean_faq_data()
    product_df = clean_product_data()

    save_dataset(faq_df, FAQ_OUTPUT)
    save_dataset(product_df, PRODUCT_OUTPUT)

    print("\n========== CLEANING SUMMARY ==========")

    print(
        f"FAQ records: {len(faq_df)}"
    )

    print(
        f"Product records: {len(product_df)}"
    )

    print("\nCleaned datasets saved successfully!")

    print("\nOutput files:")
    print(FAQ_OUTPUT)
    print(PRODUCT_OUTPUT)


if __name__ == "__main__":
    main()
