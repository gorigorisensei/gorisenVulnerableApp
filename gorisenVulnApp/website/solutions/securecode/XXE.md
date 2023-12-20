In the auth.py file, take a look at the is_xml endpoint being configured.

Vulnerable code:

```
@tools.route("/is_xml", methods=['POST'])
def tools_is_xml():
    try:
        # read data from POST
        xml_raw = request.files['xml'].read()

        # create the XML parser
        parser = etree.XMLParser()

        # parse the XML data
        root = etree.fromstring(xml_raw, parser)

        # return a string representation
        xml = etree.tostring(root, pretty_print=True, encoding='unicode')
        return jsonify({'status': 'yes', 'data': xml})
    except Exception as e:
        return jsonify({'status': 'no', 'message': str(e)})

```

Simply add the "resolve_entities=False" argument when creating the etree.XMLParser.


```
parser = etree.XMLParser(resolve_entities=False)
```