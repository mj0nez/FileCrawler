from fileswitch.switch import SwitchController

class Operator:
    # fetches the files & their content, talks to a SwitchController which informs if he needs the file content
    # and then executes the transfer protocol / the method ...
    # _stations<
    controller: SwitchController
    # def register_station(self, station):
    #     self.
   
    # TODO this method should not be part of the filter class.
    # Data Source should implement this and the overall process should provide it to the filter.
    def load(self, file, encoding="UTF-8") -> str:

        with open(file, mode="r", encoding=encoding) as f:
            content = f.read()
        return content