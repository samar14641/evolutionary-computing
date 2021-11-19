from typing import Final

class Order():
    PRIOR_MAP: Final = {'HIGH': 1, 'LOW': 2}

    def __init__(self, o_id, o_prior, o_prod, o_quant) -> None:
        """Constructor to initialise the order object
        Parameters:
            o_id (int): order ID
            o_priority (str): order priority
            o_prod (str): order product
            o_quant (int): order quantity"""

        self.o_id = o_id
        self.o_prior = self.PRIOR_MAP[o_prior]
        self.o_prod = o_prod
        self.o_quant = o_quant

    def oid(self) -> int:
        """Get order ID
        Returns:
            int: order ID"""

        return self.o_id

    def oprior(self) -> int:
        """Get order priority
        Returns:
            int: order priority as an int"""

        return self.o_prior

    def oprod(self) -> str:
        """Get order product
        Returns:
            str: order product"""

        return self.o_prod

    def oquant(self) -> int:
        """Get order quantity
        Returns:
            int: order quantity"""

        return self.o_quant

    def get_props(self) -> tuple:
        """Get order properties as a tuple
        Returns:
            tuple: the order properties"""

        return (self.o_id, self.o_prior, self.o_prod, self.o_quant)