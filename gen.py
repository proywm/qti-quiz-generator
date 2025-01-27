import csv
import os

def create_qti_question(item_id, title, question, choices, correct_choice, output_dir):
    """
    Create a QTI v2.1 XML file for a single quiz question.
    """
    qti_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1" identifier="{item_id}" title="{title}" adaptive="false" timeDependent="false">
  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
    <correctResponse>
      <value>{correct_choice}</value>
    </correctResponse>
  </responseDeclaration>
  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
    <defaultValue>
      <value>0</value>
    </defaultValue>
    <normalMaximum>1</normalMaximum>
  </outcomeDeclaration>
  <itemBody>
    <p>{question}</p>
    <choiceInteraction responseIdentifier="RESPONSE" shuffle="false" maxChoices="1">
"""
    for ident, choice_text in choices.items():
        qti_template += f"""      <simpleChoice identifier="{ident}">{choice_text}</simpleChoice>\n"""

    qti_template += """    </choiceInteraction>
  </itemBody>
  <responseProcessing template="http://www.imsglobal.org/question/qti_v2p1/rptemplates/match_correct" />
</assessmentItem>
"""

    # Write to file
    item_path = os.path.join(output_dir, f"{item_id}.xml")
    with open(item_path, "w", encoding="utf-8") as file:
        file.write(qti_template)

def generate_manifest(items, output_dir):
    """
    Generate a QTI-compliant manifest file referencing all items.
    """
    manifest_template = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest identifier="Manifest_qtiv2p1_EntryTest"
xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1
http://www.imsglobal.org/xsd/qti/qtiv2p1/qtiv2p1_imscpv1p2_v1p0.xsd
http://ltsc.ieee.org/xsd/LOM  
http://www.imsglobal.org/xsd/imsmd_loose_v1p3p2.xsd 
http://www.imsglobal.org/xsd/imsqti_metadata_v2p1
http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_metadata_v2p1p1.xsd">
  <metadata>
    <schema>QTIv2.1 Package</schema>
    <schemaversion>1.0.0</schemaversion>
    <lom xmlns="http://ltsc.ieee.org/xsd/LOM">
      <educational>
        <learningResourceType>
          <source>QTIv2.1</source>
          <value>QTI Package</value>
        </learningResourceType>
      </educational>
      <general>
        <identifier>
          <entry>Manifest_qtiv2p1_EntryTest</entry>
        </identifier>
        <title>
          <string>Generated Quiz Questions</string>
        </title>
      </general>
      <lifeCycle>
        <contribute />
        <version>
          <string>1.0</string>
        </version>
      </lifeCycle>
    </lom>
  </metadata>
  <organizations />
  <resources>
"""
    for item_id, href in items:
        manifest_template += f"""    <resource type="imsqti_item_xmlv2p1" identifier="{item_id}" href="{href}">
      <metadata>
        <lom xmlns="http://ltsc.ieee.org/xsd/LOM">
          <general>
            <identifier>
              <entry>{item_id}</entry>
            </identifier>
            <title>{item_id} Question</title>
          </general>
        </lom>
      </metadata>
      <file href="{href}" />
    </resource>
"""
    manifest_template += """  </resources>
</manifest>
"""
    manifest_path = os.path.join(output_dir, "imsmanifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as file:
        file.write(manifest_template)

def process_csv_and_generate_qti(csv_file, base_dir):
    """
    Process a CSV file with quiz questions and generate QTI v2.1 files for each question.
    """
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    items = []

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            item_id = row.get("Item ID", "").strip()
            title = row.get("Title", "").strip()
            question = row.get("Question", "").strip()
            correct_choice = row.get("Correct Choice", "").strip()
            
            # Parse choices
            choices = {}
            for col, value in row.items():
                if col and col.startswith("Choice") and value:
                    choice_id = col[-1]  # Extract A, B, C, etc.
                    choices[choice_id] = value.strip()
            
            # Validate required fields
            if not item_id or not question or not correct_choice or not choices:
                print(f"Skipping invalid row: {row}")
                continue
            
            # Create directory for item if it doesn't exist
            item_dir = os.path.join(base_dir, "Items", f"Item_{item_id}")
            os.makedirs(item_dir, exist_ok=True)
            
            # Generate QTI file for this question
            create_qti_question(item_id, title, question, choices, correct_choice, item_dir)
            
            # Track items for manifest
            items.append((item_id, f"Items/Item_{item_id}/{item_id}.xml"))
    
    # Generate the manifest file
    generate_manifest(items, base_dir)

if __name__ == "__main__":
    # CSV file path
    csv_file_path = "quiz_questions.csv"  # Update this path to your actual CSV file location
    # Base directory for generated files
    base_output_dir = "output_qti"

    # Process CSV and generate QTI files and manifest
    process_csv_and_generate_qti(csv_file_path, base_output_dir)
    print(f"QTI files and manifest generated in {base_output_dir}")
