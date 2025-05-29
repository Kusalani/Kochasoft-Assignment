import re
import requests

def my_simple_experiment():
    """Test: Can we actually find and access SAP Notes?"""
    
    # Sample text from what might be in the PDF
    sample_text = "See SAP Note 2777782 for HANA config. Also check SAP Note 1943937."
    
    # Step 1: Extract SAP Notes using regex
    pattern = re.compile(r'SAP Note (\d+)', re.IGNORECASE)
    sap_notes = pattern.findall(sample_text)
    print(f"🔍 Found SAP Notes: {sap_notes}")
    
    # Step 2: Try to access them
    accessible_count = 0
    for note_id in sap_notes:
        try:
            url = f"https://launchpad.support.sap.com/#/notes/{note_id}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ SAP Note {note_id}: Accessible")
                accessible_count += 1
            else:
                print(f"🔒 SAP Note {note_id}: Protected (HTTP {response.status_code})")
        except:
            print(f"❌ SAP Note {note_id}: Failed to access")
    
    # Step 3: Calculate success rate
    success_rate = (accessible_count / len(sap_notes)) * 100 if sap_notes else 0
    print(f"\n📊 Result: {accessible_count}/{len(sap_notes)} accessible ({success_rate:.0f}%)")
    
    return accessible_count, len(sap_notes)