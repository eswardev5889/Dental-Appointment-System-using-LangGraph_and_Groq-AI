import pandas as pd
from langchain_core.tools import tool

from dental_agent.config.settings import CSV_PATH


# =========================================================
# Helper Functions
# =========================================================

def _load_df() -> pd.DataFrame:
    """
    Load and normalize the appointment CSV data.
    """

    df = pd.read_csv(CSV_PATH)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Normalize values
    df["is_available"] = (
        df["is_available"]
        .astype(str)
        .str.upper()
        .eq("TRUE")
    )

    df["date_slot"] = pd.to_datetime(
        df["date_slot"],
        errors="coerce"
    )

    df["doctor_name"] = (
        df["doctor_name"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df["specialization"] = (
        df["specialization"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df["patient_to_attend"] = (
        df["patient_to_attend"]
        .astype(str)
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
    )

    return df


def _format_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert datetime column into readable string format.
    """

    if "date_slot" in df.columns:
        df["date_slot"] = df["date_slot"].dt.strftime(
            "%m/%d/%Y %H:%M"
        )

    return df


# =========================================================
# Tools
# =========================================================

@tool ("get_available_slots")
def get_available_slots(
    specialization: str = "",
    doctor_name: str = "",
    date_filter: str = "",
) -> list:
    """
    Get available dental appointment slots.

    Args:
        specialization:
            Dentist specialization such as 'orthodontist'.

        doctor_name:
            Specific doctor name.

        date_filter:
            Date string like '5/10/2026'.

    Returns:
        List of available appointment slots.
    """

    df = _load_df()

    mask = df["is_available"]

    # Apply specialization filter
    if specialization:
        mask &= (
            df["specialization"]
            == specialization.lower().strip()
        )

    # Apply doctor filter
    if doctor_name:
        mask &= (
            df["doctor_name"]
            == doctor_name.lower().strip()
        )

    # Apply date filter
    if date_filter:
        try:
            target_date = pd.to_datetime(
                date_filter,
                errors="coerce"
            ).date()

            mask &= (
                df["date_slot"].dt.date == target_date
            )

        except Exception:
            pass

    result = df.loc[
        mask,
        ["date_slot", "specialization", "doctor_name"]
    ].copy()

    result = _format_dates(result)

    return (
        result.head(20)
        .fillna("")
        .to_dict(orient="records")
    )


@tool("get_patient_appointments")
def get_patient_appointments(
    patient_id: str
) -> list:
    """
    Get all appointments for a patient.

    Args:
        patient_id:
            Patient ID string.

    Returns:
        List of appointments.
    """

    df = _load_df()

    mask = (
        df["patient_to_attend"]
        == str(patient_id).strip()
    )

    result = df.loc[
        mask,
        [
            "date_slot",
            "specialization",
            "doctor_name",
            "patient_to_attend",
        ]
    ].copy()

    result = _format_dates(result)

    return (
        result.fillna("")
        .to_dict(orient="records")
    )


@tool("check_slot_availability")
def check_slot_availability(
    doctor_name: str,
    date_slot: str,
) -> dict:
    """
    Check whether a doctor appointment slot is available.

    Args:
        doctor_name:
            Doctor name.

        date_slot:
            Appointment datetime.

    Returns:
        Availability details dictionary.
    """

    df = _load_df()

    target_dt = pd.to_datetime(
        date_slot,
        errors="coerce"
    )

    if pd.isna(target_dt):
        return {
            "found": False,
            "is_available": False,
            "patient_to_attend": "",
        }

    mask = (
        (df["doctor_name"]
         == doctor_name.lower().strip())
        &
        (df["date_slot"] == target_dt)
    )

    rows = df.loc[mask]

    if rows.empty:
        return {
            "found": False,
            "is_available": False,
            "patient_to_attend": "",
        }

    row = rows.iloc[0]

    return {
        "found": True,
        "is_available": bool(row["is_available"]),
        "patient_to_attend": row["patient_to_attend"],
    }


@tool("lists_doctors_by_specialization")
def list_doctors_by_specialization(
    specialization: str
) -> list:
    """
    Get all doctors for a specialization.

    Args:
        specialization:
            Dental specialization.

    Returns:
        List of doctor names.
    """

    df = _load_df()

    mask = (
        df["specialization"]
        == specialization.lower().strip()
    )

    doctors = (
        df.loc[mask, "doctor_name"]
        .dropna()
        .unique()
        .tolist()
    )

    return sorted(doctors)