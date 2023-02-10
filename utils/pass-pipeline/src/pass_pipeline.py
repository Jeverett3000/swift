class Pass(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<pass name={self.name}>"


PassListId = 0


class PassList(object):

    def __init__(self, transforms):
        global PassListId
        self.pass_id = PassListId
        PassListId += 1
        self.transforms = transforms

    def __repr__(self):
        return f"<passlist id={self.pass_id} values={self.transforms}>"

    def __iter__(self):
        return self.transforms.__iter__()

    def add_pass(self, p):
        if isinstance(p, list):
            p = PassList(p)
        self.transforms.append(p)

    def generate(self):
        stack = list(reversed(self.transforms))
        result = []
        while stack:
            transform = stack.pop()
            if isinstance(transform, Pass):
                result.append(transform.name)
                continue

            stack.extend(iter(reversed(list(transform))))
        return result


class PassPipeline(object):

    def __init__(self, identifier, action):
        self.identifier = identifier
        self.action = action
        self.pass_list = PassList([])

    def add_pass(self, p):
        self.pass_list.add_pass(p)

    def __repr__(self):
        return f"<passpipeline values={self.pass_list}>"

    def generate(self):
        x = [self.identifier, self.action['name'], self.action.get('count', 0)]
        x.extend(self.pass_list.generate())
        return x
