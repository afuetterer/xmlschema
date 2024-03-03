#!/usr/bin/env python

def main() -> None:
    from typing import Iterator, Union, cast

    from xmlschema import XMLSchema
    from xmlschema.validators import XsdSimpleType, XsdComplexType, XsdAnyElement
    from xmlschema.xpath import XPathElement

    from elementpath.protocols import XsdTypeProtocol, XsdElementProtocol, \
        XsdAttributeProtocol, GlobalMapsProtocol, XsdSchemaProtocol

    ###
    # Test protocols for XSD type annotations
    BaseXsdType = Union[XsdSimpleType, XsdComplexType]

    class Base:
        xsd_type: XsdTypeProtocol

        def __init__(self, xsd_type: XsdTypeProtocol) -> None:
            self.xsd_type = xsd_type

    class Derived(Base):
        def __init__(self, xsd_type: BaseXsdType) -> None:
            super().__init__(xsd_type)

    def check_elem_type(xsd_element: XsdElementProtocol) -> None:
        assert xsd_element.type is not None

    def check_any_elem_type(xsd_element: XsdElementProtocol) -> None:
        assert xsd_element.type is None

    def check_attr_type(xsd_attribute: XsdAttributeProtocol) -> bool:
        return xsd_attribute.type is not None

    def check_simple_type(xsd_type: XsdTypeProtocol) -> bool:
        return xsd_type.is_simple()

    def check_maps(maps: GlobalMapsProtocol) -> bool:
        return maps is not None

    def check_xsd_schema(s: XsdSchemaProtocol) -> None:
        assert s is not None

    schema = XMLSchema("""
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="elem1" type="xs:string"/>
            <xs:element name="elem2" type="xs:int"/>
            <xs:simpleType name="type1">
                <xs:restriction base="xs:string"/>
            </xs:simpleType>
            <xs:group name="group1">
                <xs:sequence>
                    <xs:any processContents="lax"/>
                </xs:sequence>
            </xs:group>
            <xs:attribute name="attr1" type="xs:int"/>
            <xs:attribute name="attr2" type="xs:float"/>
        </xs:schema>""")

    check_any_elem_type(cast(XsdAnyElement, schema.groups['group1'][0]))

    check_elem_type(schema.elements['elem1'])

    check_maps(schema.maps)

    check_xsd_schema(schema)

    a = cast(BaseXsdType, schema.types['type1'])
    check_simple_type(a)

    b = schema.attributes['attr1']
    check_attr_type(b)

    check_elem_type(XPathElement('elem4', xsd_type=a))


if __name__ == '__main__':
    main()
