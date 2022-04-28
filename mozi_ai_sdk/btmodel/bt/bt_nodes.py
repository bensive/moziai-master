# by aie


class BT:
    def __init__(self):
        self.results = {'success': "success", 'fail': "fail", 'wait': "wait", 'error': "error"}
        self.children = {}
        self.guid = None
        self.shortKey = None
        self.options = None
        self.run = None  # 把所有的动作都化简为run
        self.name = None
        self.current = None

    # 把结果转换为 self.results的结果， If false, return fail, anything else, return success
    def wrap(self, value):
        for k, v in self.results.items():
            if value == k:
                return v
        if not value:
            return self.results['fail']
        return self.results['success']

    def set_action(self, action, guid, shortKey, options):  # 其他的参数有什么用
        self.guid = guid
        self.shortKey = shortKey
        self.options = options
        self.run = action
        self.name = str(action)

    def add_child(self, child):
        # self.children.update(child)
        n = len(self.children)
        self.children[n + 1] = child

    def sequence(self, side_name, scenario):
        for k, v in self.children.items():
            if self.wrap(v.run(side_name, scenario)) == self.results['fail']:
                return self.results['fail']
        return self.results['success']

    def select(self, side_name, scenario):
        for k, v in self.children.items():
            if self.wrap(v.run(side_name, scenario)) == self.results['success']:
                return self.results['success']
        return self.results['fail']

    def slice_sequence(self, side_name, scenario):
        if self.current is None:
            self.current = 1
        else:
            child = self.children[self.current]
            if child is None:
                self.current = 1
                return self.results['success']
            result = self.wrap(child.run(side_name, scenario))
            if result == self.results['fail']:
                self.current = 1
                return self.results['fail']
            if result == self.results['success']:
                self.current = self.current + 1
        return self.results['wait']

    # 在案例里边，时间切片是否执行
    def slice_select(self, side_name, scenario):
        if self.current is None:
            self.current = 1
        else:
            child = self.children[self.current]
            if child is None:
                self.current = 1
                return self.results['fail']
            result = self.wrap(child.run(side_name, scenario))
            if result == self.results['success']:
                self.current = 1
                return self.results['success']
            if result == self.results['fail']:
                self.current = self.current + 1
        return self.results['wait']

    def invert(self, side_name, scenario):
        if self.children[1] is None:
            return self.results['success']
        result = self.wrap(self.children[1].run(side_name, scenario))
        if result == self.results['success']:
            return self.results['fail']
        if result == self.results['fail']:
            return self.results['success']
        return result

    def repeat_until_fail(self, side_name, scenario):
        while self.wrap(self.children[1].run(side_name, scenario)) != self.results['fail']:
            pass
        return self.results['success']

    def wait_until_fail(self, side_name, scenario):
        if self.wrap(self.children[1].run(side_name, scenario)) == self.results['fail']:
            return self.results['success']
        return self.results['wait']
