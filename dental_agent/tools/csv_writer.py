import pandas as pd

from langchain_core.tools import tool

from dental_agent.config.settings import CSV_PATH


# =========================================================
# Helpers
# =========================================================

DATE_OUTPUT_FORMAT = "%m/%d/%Y %H:%M"


def _parse_datetime(value: str):
    """
    Safely parse datetime string.
    """
    return pd.to_datetime(value, errors="coerce")


def _success(message: str) -> dict:
    return {
        "success": True,
        "message": message,
    }


def _error(message: str) -> dict:
    return {
        "success": False,
        "message": message,
    }


def _load_df() -> pd.DataFrame:
    """
    Load and normalize appointment data.
    """

    df = pd.read_csv(CSV_PATH)

    df.columns = df.columns.str.strip()

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


def _save_df(df: pd.DataFrame) -> None:
    """
    Save normalized dataframe back to CSV.
    """

    out = df.copy()

    out["date_slot"] = out["date_slot"].dt.strftime(
        DATE_OUTPUT_FORMAT
    )

    out["is_available"] = out["is_available"].map({
        True: "TRUE",
        False: "FALSE",
    })

    out["patient_to_attend"] = (
        out["patient_to_attend"]
        .fillna("")
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
    )

    out.to_csv(CSV_PATH, index=False)


# =========================================================
# Booking Tool
# =========================================================

@tool("book_appointment")
def book_appointment(
    patient_id: str,
    doctor_name: str,
    date_slot: str,
) -> dict:
    """
    Book a dental appointment.
    """

    df = _load_df()

    target_dt = _parse_datetime(date_slot)

    if pd.isna(target_dt):
        return _error(
            f"Invalid date format: {date_slot}"
        )

    doctor = doctor_name.lower().strip()
    patient = str(patient_id).strip()

    mask = (
        (df["doctor_name"] == doctor)
        &
        (df["date_slot"] == target_dt)
    )

    rows = df.loc[mask]

    if rows.empty:
        return _error(
            "Appointment slot not found."
        )

    if not rows.iloc[0]["is_available"]:
        return _error(
            "Appointment slot is already booked."
        )

    df.loc[mask, "is_available"] = False
    df.loc[mask, "patient_to_attend"] = patient

    _save_df(df)

    return _success(
        f"Appointment booked for patient "
        f"{patient_id} with {doctor_name} "
        f"at {date_slot}."
    )


# =========================================================
# Cancellation Tool
# =========================================================

@tool("cancel_appointment")
def cancel_appointment(
    patient_id: str,
    date_slot: str,
) -> dict:
    """
    Cancel an existing appointment.
    """

    df = _load_df()

    target_dt = _parse_datetime(date_slot)

    if pd.isna(target_dt):
        return _error(
            f"Invalid date format: {date_slot}"
        )

    patient = str(patient_id).strip()

    mask = (
        (df["patient_to_attend"] == patient)
        &
        (df["date_slot"] == target_dt)
        &
        (~df["is_available"])
    )

    rows = df.loc[mask]

    if rows.empty:
        return _error(
            f"No appointment found for "
            f"patient {patient_id}."
        )

    df.loc[mask, "is_available"] = True
    df.loc[mask, "patient_to_attend"] = ""

    _save_df(df)

    return _success(
        f"Appointment for patient "
        f"{patient_id} at {date_slot} "
        f"has been cancelled."
    )


# =========================================================
# Reschedule Tool
# =========================================================

@tool("reschedule_appointment")
def reschedule_appointment(
    patient_id: str,
    current_date_slot: str,
    new_date_slot: str,
    doctor_name: str,
) -> dict:
    """
    Reschedule an appointment.
    """

    df = _load_df()

    current_dt = _parse_datetime(current_date_slot)
    new_dt = _parse_datetime(new_date_slot)

    if pd.isna(current_dt):
        return _error(
            f"Invalid current slot: "
            f"{current_date_slot}"
        )

    if pd.isna(new_dt):
        return _error(
            f"Invalid new slot: "
            f"{new_date_slot}"
        )

    patient = str(patient_id).strip()
    doctor = doctor_name.lower().strip()

    # Existing appointment
    old_mask = (
        (df["patient_to_attend"] == patient)
        &
        (df["date_slot"] == current_dt)
        &
        (~df["is_available"])
    )

    if df.loc[old_mask].empty:
        return _error(
            f"No existing appointment found "
            f"for patient {patient_id}."
        )

    # New slot
    new_mask = (
        (df["doctor_name"] == doctor)
        &
        (df["date_slot"] == new_dt)
    )

    new_rows = df.loc[new_mask]

    if new_rows.empty:
        return _error(
            f"New slot does not exist "
            f"for doctor {doctor_name}."
        )

    if not new_rows.iloc[0]["is_available"]:
        return _error(
            f"New slot {new_date_slot} "
            f"is already booked."
        )

    # Release old slot
    df.loc[old_mask, "is_available"] = True
    df.loc[old_mask, "patient_to_attend"] = ""

    # Assign new slot
    df.loc[new_mask, "is_available"] = False
    df.loc[new_mask, "patient_to_attend"] = patient

    _save_df(df)

    return _success(
        f"Appointment for patient "
        f"{patient_id} rescheduled from "
        f"{current_date_slot} to "
        f"{new_date_slot} with "
        f"{doctor_name}."
    )