import numpy as np
import re

class MSC:
    """
    Maximum Similiraty Counter or MSC compute the similarity between two texts.
    Result is contain in [0, 1].
    1 -> texts are stricly equals
    0 -> texts are stricly different

    ## attributes
    - version: current of version of the object
    - verbose: true if you want display informations, false oftherwise. Default false:

    ## Using:

    TXT1 = "Hello i teach physics in Oxford."
    TXT2 = "Hello i teach physics at MIT"

    msc = MSC(verbose=True)
    msc.similarity(TXT1, TXT2)
    >>> 0.670425981359072

    """
    def __init__(self, verbose = False):
        """
        Maximum Similarity counter constructor.
        """
        self.__version__ = "0.0.1"
        self.verbose = verbose
    
    def kernel(self, x = 0, s = 1):
        """
        Compute the following formula:

        $exp^{- 0.5 * \frac{x^2}{s^2}}

        This is statistical Gauss Kernel.

        ## Inputs:
        - x (float): mandatory, input. Default 0
        - s (float): mandatory, accuracy parameter. Default 1

        ## Ouputs:
        - float
        """
        return np.exp( - 0.5 * x ** 2 / s ** 2)

    def S(self, X = [0]):
        """
        Compute the mean of kernel results of X.

        ## Inputs:
        - X (list of float): mandatory, input. Default [0]

        ## Ouputs:
        - float
        """

        return np.sum(self.kernel(X)) / len(X)

    def _ord(self, text = "default text"):
        """
        Compute each letter ASCII equivalent of the text.

        ## Input:
        - text (str): mandatory, a text to convert in ASCII 

        ## Ouput:
        - a list of integer
        """
        return list(map(ord, text))

    def equalizeTexts(self, text1 = "A long text", text2 = "a text"):
        """
        Add chr(0) = '\x00' at the end of the shorter text. The goal is to
        have the same lenght for text1 and text2.

        ## Inputs:
        - text1 (str): mandatory, first text. Default 'a long text'
        - text2 (str): mandaotry, second text. Default 'a text' (shorter than text1)

        ## Ouputs:
        - a tuple with same length text1 and text2
        """

        n1 = len(text1.split(" "))
        n2 = len(text2.split(" "))

        if n1 > n2:
            n = n1 - n2
            text2 += " ".join(chr(0) for _ in range(n))
        else:
            n = n2 - n1
            text1 += " ".join(chr(0) for _ in range(n))

        return text1, text2

    def similarity(self, text1, text2):
        """
        Return the similiraty between text1 and text2.
        If similarity is :
        - 1 -> text1 and text2 are stricly equal
        - 0 -> text1 and text2 are complety different

        ## Inputs:
        - text1 (str): mandatory, a text
        - text2 (str): mandatory, an other text

        ## Ouputs:
        - float, the similiraty between text1 and text2
        """

        # clean up both texts
        text1 = self.clean(text1)
        text2 = self.clean(text2)
        text1, text2 = self.equalizeTexts(text1, text2)

        sim = []
        for word1, word2 in zip(text1.split(" "), text2.split(" ")):


            int1 = self._ord(word1)
            int2 = self._ord(word2)

            # equalize word1 and word2. Same process as 'equalizeText' method
            # but to have the same length for word1 and word2
            n1 = len(int1)
            n2 = len(int2)

            if n1 > n2:
                n = n1 - n2
                int2 += [0 for _ in range(n)]
            else:
                n = n2 - n1
                int1 += [0 for _ in range(n)]

            int1 = np.array(int1)
            int2 = np.array(int2)

            z = int2 - int1
            s = self.S(z)

            if self.verbose:
                print("{0} {1} {2} {3}".format(word1, word2, z, s))

            sim.append(s)
            
        return np.mean(sim)

    def clean(self, text = "default text héhè"):
        """
        Clean up the input text. 
        Replace 'é' by 'e'
        Replace 'è' by 'e'
        Replace '\n' by ' '
        Strip left, rigth and middle spaces

        ## Inputs:
        - text (str): mandatory, text to clean up. Default = 'default text héhè'

        ## Ouputs:
        - the clean up text
        """
        text = text.lower()
        text = text.replace("é", "e")
        text = text.replace("è", "e")
        text = text.replace("\n", " ")
        text = text.strip()
        text = re.sub(' +', ' ', text)

        outText = ""
        for letter in text:
            if 97 <= ord(letter) <= 122 or 48 <= ord(letter) <= 57 or letter == " ":
                outText += letter

        return outText

class MSCMultiple:
    """
    Maximum Similiraty Counter for multiple field or MSCm compute the similarity
    between two texts of the same field.
    Result is contain in [0, 1].
    1 -> all fields are stricly equal
    0 -> all fields are strictly different

    ## attributes
    - version: current of version of the object
    - verbose: true if you want display informations, false oftherwise. Default false:

    ## Using:

    TXT1 = "Hello i teach physics in Oxford."
    TXT2 = "Hello i teach physics at MIT"
    TXT11 = "england"
    TXT22 = "USA"

    msc = MSC(verbose=True)
    msc.similarity([TXT1, TXT11], [TXT2, TXT22])
    >>> 0.335213257956904

    """
    def __init__(self, verbose):
        self.__version__ = "0.0.1"
        self.verbose = verbose

    def similarity(self, fields1, fields2):
        """
        Compute the similiratiry between two list of same fields.

        ## Inputs:
        - fields1 (list of str): mandatory, a list of string with n fields
        - fields2 (list of str): mandatory, an other list of string with the same number of fields

        ## Ouputs:
        - float, the mean of similiraty of each fields.
        """
        msc = MSC(verbose=self.verbose)
        sim = []
        for field1, field2 in zip(fields1, fields2):
            s = msc.similarity(field1, field2)
            sim.append(s)

        return np.mean(sim)

if __name__ == "__main__":

    # simple text comparison

    TXT1 = "Hello i teach physics in Oxford."
    TXT2 = "Hello i teach physics at MIT"

    msc = MSC(verbose=True)
    s = msc.similarity(TXT1, TXT2)
    print(s)

    # multiple texts comparison

    TXT1 = "Hello i teach physics in Oxford."
    TXT2 = "Hello i teach physics at MIT"
    TXT11 = "england"
    TXT22 = "USA"

    mscm = MSCMultiple(verbose=True)
    s = mscm.similarity([TXT1, TXT11], [TXT2, TXT22])
    print(s)
