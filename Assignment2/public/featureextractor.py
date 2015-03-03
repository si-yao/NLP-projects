from nltk.compat import python_2_unicode_compatible

printed = False
'''
token has following keys:
word, lemma, ctag, tag, feats, head, rel
'''

@python_2_unicode_compatible
class FeatureExtractor(object):
    @staticmethod
    def _check_informative(feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """

        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    @staticmethod
    def find_left_right_dependencies(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most


    @staticmethod
    def find_left_right_idx(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r

        return left_most, right_most

    @staticmethod
    def extract_features0(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        global printed
        if not printed:
            print("This is not a very good feature extractor!")
            printed = True

        # an example set of features:
        if stack:
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            # @Siyao: it is better to add XXX_NULL if this feature doesn't exsit!!!
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('STK_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)

            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('STK_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('STK_0_RDEP_' + dep_right_most)

        if buffer:
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)

            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('BUF_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('BUF_0_RDEP_' + dep_right_most)

        return result


    @staticmethod
    def extract_features1(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        global printed
        if not printed:
            print("This is 1st feature extractor!")
            printed = True

        #features I use
        stk0Form = buf0Form = buf1Form = stk0Ldep = stk0Rdep = buf0Ldep = buf0Rdep = '_'

        # an example set of features:
        if stack:
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            # @Siyao: it is better to add XXX_NULL if this feature doesn't exsit!!!
            if FeatureExtractor._check_informative(token['word'], True):
                stk0Form = token['word']


            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                stk0Ldep = dep_left_most
            if FeatureExtractor._check_informative(dep_right_most):
                stk0Rdep = dep_right_most

        if buffer:
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                buf0Form = token['word']

            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                buf0Ldep = dep_left_most
            if FeatureExtractor._check_informative(dep_right_most):
                buf0Rdep = dep_right_most
            if len(buffer) > 1:
                buffer_idx1 = buffer[1]
                token = tokens[buffer_idx1]
                if FeatureExtractor._check_informative(token['word'], True):
                    buf1Form = token['word']
            result.append('STK_0_FORM_'+stk0Form)
            result.append('STK_0_LDEP_'+stk0Ldep)
            result.append('STK_0_RDEP_'+stk0Rdep)
            result.append('BUF_0_FORM_'+buf0Form)
            result.append('BUF_0_LDEP_'+buf0Ldep)
            result.append('BUF_0_RDEP_'+buf0Rdep)
            result.append('BUF_1_FORM_'+buf1Form)
        return result

    @staticmethod
    def extract_features(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        global printed
        if not printed:
            print("This is 2nd feature extractor!")
            printed = True

        #features I use
        stk0Form = stk0Ldep = stk0Rdep = stk0Lemma = stk0Postag = stk0tag = stk0Feats = stk1Postag = stk1tag = '_'
        buf0Form = buf0Ldep = buf0Rdep = buf0Lemma = buf0Postag = buf0tag = buf0Feats = buf1Form = buf1Postag = buf1tag = buf2Postag = buf2tag = buf3Postag = '_'
        #stk0RdepTag = stk0LdepTag = buf0RdepTag = buf0LdepTag = '_'
        #stk0RdepForm = stk0LdepForm = buf0RdepForm = buf0LdepForm = '_'
        #buf2Form = '_'
        '''
        token has following keys:
        word, lemma, ctag, tag, feats, Xhead, Xrel
        '''
        # an example set of features:
        if stack:
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            # @Siyao: it is better to add XXX_NULL if this feature doesn't exsit!!!
            if FeatureExtractor._check_informative(token['word'], True):
                stk0Form = token['word']
            if FeatureExtractor._check_informative(token['lemma'], True):
                stk0Lemma = token['lemma']
            if FeatureExtractor._check_informative(token['tag'], True):
                stk0Postag = token['tag']
            if FeatureExtractor._check_informative(token['ctag'], True):
                stk0tag = token['ctag']

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)
            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)
            idx_left_most, idx_right_most = FeatureExtractor.find_left_right_idx(stack_idx0, arcs)
            if idx_left_most < 1000000:
                t = tokens[idx_left_most]['word']
                if FeatureExtractor._check_informative(t, True):
                    stk0LdepForm = t
            if idx_right_most > -1:
                t = tokens[idx_right_most]['word']
                if FeatureExtractor._check_informative(t, True):
                    stk0RdepForm = t


            if FeatureExtractor._check_informative(dep_left_most):
                stk0Ldep = dep_left_most
            if FeatureExtractor._check_informative(dep_right_most):
                stk0Rdep = dep_right_most

            if len(stack)>1:
                token = tokens[stack[-2]]
                if FeatureExtractor._check_informative(token['tag'], True):
                    stk1Postag = token['tag']
                if FeatureExtractor._check_informative(token['ctag'], True):
                    stk1tag = token['ctag']


        if buffer:
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                buf0Form = token['word']
            if FeatureExtractor._check_informative(token['lemma'], True):
                buf0Lemma = token['lemma']
            if FeatureExtractor._check_informative(token['tag'], True):
                buf0Postag = token['tag']
            if FeatureExtractor._check_informative(token['ctag'], True):
                buf0tag = token['ctag']


            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)

            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)
            idx_left_most, idx_right_most = FeatureExtractor.find_left_right_idx(buffer_idx0, arcs)
            if idx_left_most < 1000000:
                t = tokens[idx_left_most]['word']
                if FeatureExtractor._check_informative(t, True):
                    buf0LdepForm = t
            if idx_right_most > -1:
                t = tokens[idx_right_most]['word']
                if FeatureExtractor._check_informative(t, True):
                    buf0RdepForm = t


            if FeatureExtractor._check_informative(dep_left_most):
                buf0Ldep = dep_left_most
            if FeatureExtractor._check_informative(dep_right_most):
                buf0Rdep = dep_right_most
            if len(buffer) > 1:
                buffer_idx1 = buffer[1]
                token = tokens[buffer_idx1]
                if FeatureExtractor._check_informative(token['word'], True):
                    buf1Form = token['word']
                if FeatureExtractor._check_informative(token['ctag'], True):
                    buf1Postag = token['ctag']
            if len(buffer) > 2:
                token = tokens[buffer[2]]
                if FeatureExtractor._check_informative(token['tag'], True):
                    buf2Postag = token['tag']
                if FeatureExtractor._check_informative(token['ctag'], True):
                    buf2tag = token['ctag']
                if FeatureExtractor._check_informative(token['word'], True):
                    buf2Form = token['word']
            if len(buffer) > 3:
                token = tokens[buffer[3]]
                if FeatureExtractor._check_informative(token['tag'], True):
                    buf3Postag = token['tag']
                if FeatureExtractor._check_informative(token['ctag'], True):
                    buf3tag = token['ctag']

            result.append('STK_0_FORM_'+stk0Form)
            result.append('STK_0_LDEP_'+stk0Ldep)
            result.append('STK_0_RDEP_'+stk0Rdep)
            result.append('STK_0_LEMMA_'+stk0Lemma)
            result.append('STK_0_TAG_'+stk0Postag)
            result.append('STK_1_TAG_'+stk1Postag)

            result.append('BUF_0_FORM_'+buf0Form)
            result.append('BUF_0_LDEP_'+buf0Ldep)
            result.append('BUF_0_RDEP_'+buf0Rdep)
            result.append('BUF_0_LEMMA_'+buf0Lemma)
            result.append('BUF_0_TAG_'+buf0Postag)

            result.append('BUF_1_TAG_'+buf1Postag)
            result.append('BUF_1_FORM_'+buf1Form)
            result.append('BUF_2_TAG_'+buf2Postag)
            #result.append('BUF_2_FORM_'+buf2Form)
            #result.append('BUF_3_TAG_'+buf3Postag) bad feature
            #result.append("STK_0_CTAG_"+stk0tag)
            #result.append("STK_1_CTAG_"+stk1tag)
            #result.append("BUF_0_CTAG"+buf0tag)
            #result.append("BUF_1_CTAG"+buf1tag)
            #result.append("BUF_2_CTAG"+buf2tag)
            #result.append('STK_0_LDEPFORM_'+stk0LdepForm)
            #result.append('STK_0_RDEPFORM_'+stk0RdepForm)
            #result.append('BUF_0_LDEPFORM_'+buf0LdepForm)
            #result.append('BUF_0_RDEPFORM_'+buf0RdepForm)
        return result