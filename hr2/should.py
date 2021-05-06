

class ShouldWrapper():
    def __init__(self, obj, name, value, testcase):
        self._words = [name, ]
        self._value = value
        self._testcase = testcase
        self._it = obj

    def __getitem__(self, key):
        return ShouldWrapper(self._it,
                             "{}[{}]".format(self.spec, key),
                             self._value[key],
                             self._testcase)

    def _push_objective(self, verb, objective):
        self._words.append(verb)
        self._words.append("{}".format(objective))

    @property
    def spec(self):
        return " ".join(self._words)
        
    @property
    def should(self):
        self._words.append("should")
        return self

    @property
    def be(self):
        self._words.append("be")
        return self

    def have(self, value):
        self._push_objective("have", value)
        self._testcase.assertIn(value, self._value, self.spec)
        return self._it

    def equal(self, value):
        self._push_objective("equal", value)
        self._testcase.assertEqual(self._value, value, self.spec)
        return self._it

class It():
    def __init__(self, obj, testcase):
        self._object = obj
        self._testcase = testcase

    @property
    def then(self):
        return self

    @property
    def and_(self):
        return self

    def __getattr__(self, name):
        return ShouldWrapper(self, name, getattr(self._object, name), self._testcase)

