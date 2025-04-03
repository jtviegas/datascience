import spacy

class UtilsNlp:
  """
  Utility class for NLP tasks.
  """

  def __init__(self):
      """
      Initialize the NLP utility class.
      """
      self._nlp = spacy.load("en_core_web_sm")

  def text2sentences(self, text):
      """
      text is broken down to sentences

      Args:
          text (str): The input text.

      Returns:
          list: A list of sentences.
      """
      doc = self._nlp(text)
      return [sentence.text for sentence in doc.sents]
  
  def tokenize(self, text):
      """
      Tokenize the input text.

      Args:
          text (str): The input text to tokenize.

      Returns:
          list: A list of tokens.
      """
      doc = self._nlp(text)
      return [token.text for token in doc]
  
  def tagWords(self, text, model=None):
      """
      tag the words in the input text.

      Args:
          text (str): The input text.

      Returns:
          list: A list of tuples with the word and the tag.
      """
      _model = model if model else self._nlp
      doc = _model(text)
      words = [token.text for token in doc]
      pos = [token.pos_ for token in doc]
      return list(zip(words, pos))
  
  def lemmatize(self, text):
      """
      Lemmatize the input text.

      Args:
          text (str): The input text.

      Returns:
          list: A list of tuples with the word and its lemma.
      """
      result = []
      doc = self._nlp(text)
      for token in doc:
        result.append((token, token.lemma_))

      return result


