from rest_framework import serializers

from .models import Card


class CardCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    ccv = serializers.IntegerField()

    def validate_card_number(self, value):
        if len(value) != 16 or not value.isdigit():
            raise serializers.ValidationError("Card number must be 16 digits long")
        return value

    def validate_ccv(self, value):
        if value < 100 or value > 999:
            raise serializers.ValidationError("CCV must be in range [100,999]")
        return value

    def check_valid(self, card_number: str, ccv: int):
        for i in range(0, 16, 4):
            x, y = int(card_number[i : i + 2]), int(card_number[i + 2 : i + 4])
            if (x ** (y**3)) % ccv % 2 != 0:
                return False
        return True
        # pairs = [
        #     (int(card_number[i : i + 2]), int(card_number[i + 2 : i + 4]))
        #     for i in range(0, len(card_number), 4)
        # ]

        # for x, y in pairs:
        #     if (x ** (y**3)) % ccv % 2 != 0:
        #         return False
        # return True

    def validate(self, attrs):
        card_number = attrs["card_number"]
        ccv = attrs["ccv"]

        attrs["is_valid"] = self.check_valid(card_number, ccv)
        attrs["censored_number"] = f"{card_number[:4]}********{card_number[-4:]}"

        return attrs

        # card_number = attrs.get("card_number", None)
        # ccv = attrs.get("ccv", None)

        # assert card_number is not None and ccv is not None

        # attrs.pop("ccv")
        # attrs.pop("card_number")

        # attrs["is_valid"] = self.check_valid(card_number, ccv)
        # attrs["censored_number"] = card_number[:4] + "*" * 8 + card_number[-4:]

        # return super().validate(attrs)

    def create(self, validated_data):
        return Card.objects.create(
            censored_number=validated_data["censored_number"],
            is_valid=validated_data["is_valid"],
            user=validated_data["user"],
        )


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["title", "censored_number", "is_valid", "created_at", "updated_at"]
