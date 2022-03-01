from django_components import component


@component.register("basic_info")
class BasicInfo(component.Component):
    template_name = "basic_info.html"

    def get_context_data(self, employee=None):
        return {
            "employee": employee,
        }


@component.register("address")
class Address(component.Component):
    template_name = "address.html"

    def get_context_data(self, employee=None):
        return {
            "employee": employee,
        }


@component.register("legal")
class Legal(component.Component):
    template_name = "legal.html"

    def get_context_data(self, employee=None):
        return {
            "employee": employee,
        }
