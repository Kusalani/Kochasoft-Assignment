"""
Test with REAL PDF content - not sample text
This will show the actual challenge
"""
import re
import requests
from llama_index.core import SimpleDirectoryReader

def test_with_real_pdf():
    """Extract SAP Notes from the actual PDF file"""
    
    # Load the actual PDF from your input directory
    try:
        loader = SimpleDirectoryReader(
            input_dir="input-dir",  # Your PDF directory
            required_exts=[".pdf"],
            recursive=True
        )
        documents = loader.load_data()
        
        print(f"📄 Loaded {len(documents)} documents")
        
        # Get text from first document
        if documents:
            pdf_text = documents[0].text
            print(f"📝 PDF text length: {len(pdf_text)} characters")
            
            # Show first 500 characters to see what's actually in there
            print(f"\n🔍 First 500 characters of PDF:")
            print(pdf_text[:500])
            print("...")
            
            # Now extract SAP Notes from REAL content
            return extract_and_test_real_sap_notes(pdf_text)
        else:
            print("No PDF documents found")
            return []
            
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return []

def extract_and_test_real_sap_notes(pdf_text):
    """Extract SAP Notes from real PDF and test access"""
    
    # Extract SAP Notes from actual PDF content
    pattern = re.compile(r'SAP[\s-]*Note[\s#]*(\d+)', re.IGNORECASE)
    sap_notes = pattern.findall(pdf_text)
    
    # Remove duplicates and sort
    unique_notes = list(set(sap_notes))
    print(f"\n🔍 Found {len(unique_notes)} unique SAP Notes in real PDF: {unique_notes}")
    
    if not unique_notes:
        print("ℹ️  No SAP Notes found in this PDF")
        return []
    
    # Test access to REAL SAP Notes
    results = []
    for note_id in unique_notes[:5]:  # Test first 5 to avoid too many requests
        try:
            url = f"https://launchpad.support.sap.com/#/notes/{note_id}"
            print(f"\n🔍 Testing SAP Note {note_id}...")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ SAP Note {note_id}: Accessible")
                results.append({"note_id": note_id, "accessible": True})
            elif response.status_code in [401, 403]:
                print(f"🔒 SAP Note {note_id}: Protected (HTTP {response.status_code})")
                results.append({"note_id": note_id, "accessible": False, "reason": "authentication_required"})
            elif response.status_code == 404:
                print(f"SAP Note {note_id}: Not found (HTTP 404)")
                results.append({"note_id": note_id, "accessible": False, "reason": "not_found"})
            else:
                print(f"SAP Note {note_id}: Unknown status (HTTP {response.status_code})")
                results.append({"note_id": note_id, "accessible": False, "reason": f"http_{response.status_code}"})
                
        except requests.exceptions.Timeout:
            print(f"⏰ SAP Note {note_id}: Timeout")
            results.append({"note_id": note_id, "accessible": False, "reason": "timeout"})
        except Exception as e:
            print(f"💥 SAP Note {note_id}: Error - {str(e)[:50]}...")
            results.append({"note_id": note_id, "accessible": False, "reason": "error"})
    
    # Summary
    accessible_count = sum(1 for r in results if r["accessible"])
    total_count = len(results)
    
    print(f"\n📊 REAL PDF RESULTS:")
    print(f"Total SAP Notes tested: {total_count}")
    print(f"Accessible: {accessible_count}")
    print(f"Protected/Failed: {total_count - accessible_count}")
    if total_count > 0:
        print(f"Real success rate: {(accessible_count/total_count)*100:.1f}%")
    
    return results

if __name__ == "__main__":
    print("Testing with REAL PDF content...")
    real_results = test_with_real_pdf()