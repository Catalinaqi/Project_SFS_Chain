from dataclasses import dataclass


@dataclass
class ThresholdEntity:
    """
    Represents operation thresholds for products.
    """
    operation_threshold: str
    product_threshold: str
    threshold_maximum: float
    tipo: str

    def __post_init__(self):
        """
        Validates values after initialization.
        """
        if not self.operation_threshold or not isinstance(self.operation_threshold, str):
            raise ValueError("Operation threshold is required.")

        if not self.product_threshold or not isinstance(self.product_threshold, str):
            raise ValueError("Product threshold is required.")

        if self.threshold_maximum < 0:
            raise ValueError("Threshold maximum cannot be negative.")

        if not self.tipo or not isinstance(self.tipo, str):
            raise ValueError("Type must be a non-empty string.")
