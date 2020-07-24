from App.apis.Dicer2Resource import Dicer2Resource


class SearchResource(Dicer2Resource):
    """ 查重相关资源的基类 """

    @classmethod
    def get_custom_configs(cls):
        search_precision = cls.get_parameter("SEARCH_PRECISION", location=["json", "form"])
        minimal_line_length = cls.get_parameter("MINIMAL_LINE_LENGTH", location=["json", "form"])
        jaccard_threshold_value = cls.get_parameter("JACCARD_THRESHOLD_VALUE", location=["json", "form"])
        image_hamming_threshold_value = cls.get_parameter("IMAGE_HAMMING_THRESHOLD_VALUE", location=["json", "form"])

        return dict(
            search_precision=search_precision,
            minimal_line_length=minimal_line_length,
            jaccard_threshold_value=jaccard_threshold_value,
            image_hamming_threshold_value=image_hamming_threshold_value
        )
