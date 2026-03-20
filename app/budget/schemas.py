from pydantic import BaseModel, field_validator


class BudgetSettingsUpdate(BaseModel):
    rate_1: float
    rate_2: float
    rate_3: float
    zus_costs: float
    accounting_costs: float
    initial_balance: float

    @field_validator("rate_1", "rate_2", "rate_3", "zus_costs", "accounting_costs")
    @classmethod
    def must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Value must be positive")
        return round(v, 2)

    @field_validator("initial_balance")
    @classmethod
    def must_be_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Value must be non-negative")
        return round(v, 2)


class BudgetSettingsResponse(BaseModel):
    id: str
    calendar_id: str
    rate_1: float
    rate_2: float
    rate_3: float
    zus_costs: float
    accounting_costs: float
    initial_balance: float

    model_config = {"from_attributes": True}
