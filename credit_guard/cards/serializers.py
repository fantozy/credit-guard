from rest_framework import serializers

from .models import Card
import math
import time


class CardCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    ccv = serializers.IntegerField()

    def validate_card_number(self, value: str):
        if len(value) != 16 or not value.isdigit():
            raise serializers.ValidationError("Card number must be 16 digits long")
        return value

    def validate_ccv(self, value: int):
        if value < 100 or value > 999:
            raise serializers.ValidationError("CCV must be in range [100,999]")
        return value

    def check_valid(self, card_number: str, ccv: int):
        """
        Check if a credit card is valid based on the card number and CCV.

        Args:
            card_number (str): The credit card number.
            ccv (int): The CCV (Card Verification Value) of the credit card.

        Returns:
            bool: True if the credit card is valid, False otherwise.
        """
        pairs = [
            (int(card_number[i : i + 2]), int(card_number[i + 2 : i + 4]))
            for i in range(0, len(card_number), 4)
        ]

        # As calculation of expressions will take a lot of time
        # for large numbers, I implemented this method to efficiently
        # calculate power of large numbers and their multiplication
        def mod_exp(base: int, exp: int, mod: int) -> int:
            """
            Calculates the modular exponentiation of a base raised to an exponent modulo a given modulus.

            Args:
                base (int): The base value.
                exp (int): The exponent value.
                mod (int): The modulus value.

            Returns:
                int: The result of the modular exponentiation.

            """
            result = 1
            while exp > 0:
                if exp % 2 == 1:
                    result = (result * base) % mod
                base = (base * base) % mod
                exp //= 2
            return result

        for x, y in pairs:
            if mod_exp(x, y**3, ccv) % 2 != 0:
                return False
        return True

    def validate(self, attrs: dict) -> dict:
        card_number = attrs["card_number"]
        ccv = attrs["ccv"]
        attrs["is_valid"] = self.check_valid(card_number, ccv)
        attrs["censored_number"] = f"{card_number[:4]}********{card_number[-4:]}"

        return attrs

    def create(self, validated_data: dict):
        return Card.objects.create(
            censored_number=validated_data["censored_number"],
            is_valid=validated_data["is_valid"],
            user=validated_data["user"],
        )


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["title", "censored_number", "is_valid", "created_at", "updated_at"]
