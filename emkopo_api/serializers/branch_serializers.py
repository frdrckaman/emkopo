from rest_framework import serializers

from emkopo_product.models import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['BranchCode', 'BranchName']
