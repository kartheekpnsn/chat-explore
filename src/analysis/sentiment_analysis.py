class Sentiment:
    MODEL_ID = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    _pipeline = None

    @classmethod
    def _get_pipeline(cls):
        if cls._pipeline is None:
            cls._pipeline = cls._build_pipeline()
        return cls._pipeline

    @classmethod
    def _build_pipeline(cls):
        from transformers import pipeline

        return pipeline(
            "sentiment-analysis",
            model=cls.MODEL_ID,
            tokenizer=cls.MODEL_ID,
            device=cls._get_device(),
            top_k=None,
        )

    @staticmethod
    def _get_device():
        import torch

        if torch.cuda.is_available():
            return 0

        mps_backend = getattr(torch.backends, "mps", None)
        if mps_backend is not None and mps_backend.is_available():
            return "mps"

        return -1

    @classmethod
    def huggingface(cls, sentence):
        """

        :param sentence:
        :return:
        """
        if not isinstance(sentence, str) or not sentence.strip():
            return 0.0

        predictions = cls._get_pipeline()(sentence)
        return cls.get_polarity_score(predictions)

    @staticmethod
    def get_polarity_score(predictions):
        scores = Sentiment._flatten_predictions(predictions)
        positive_score = 0.0
        negative_score = 0.0

        for prediction in scores:
            label = prediction.get("label", "").lower()
            score = float(prediction.get("score", 0.0))

            if label in {"positive", "label_2"}:
                positive_score = score
            elif label in {"negative", "label_0"}:
                negative_score = score

        return positive_score - negative_score

    @staticmethod
    def _flatten_predictions(predictions):
        if not predictions:
            return []
        if isinstance(predictions[0], list):
            return predictions[0]
        return predictions
