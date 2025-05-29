# Create the test file

#!/usr/bin/env python3
"""Quick test to verify all required packages are installed"""

def test_imports():
    packages_to_test = [
        ("ollama", "ollama"),
        ("neo4j", "neo4j"),
        ("pydantic", "pydantic"),
        ("redis", "redis"),
        ("llama_index.core", "llama-index core"),
        ("llama_index.llms.ollama", "llama-index ollama LLM"),
        ("llama_index.embeddings.ollama", "llama-index ollama embeddings"),
        ("llama_index.graph_stores.neo4j", "llama-index neo4j graph store"),
    ]
    
    print("Testing package imports...")
    print("-" * 50)
    
    success = []
    failed = []
    
    for package, display_name in packages_to_test:
        try:
            __import__(package)
            print(f"✅ {display_name}")
            success.append(display_name)
        except ImportError as e:
            print(f"❌ {display_name}: {e}")
            failed.append((display_name, str(e)))
    
    print("-" * 50)
    print(f"✅ Successfully imported: {len(success)}")
    print(f"❌ Failed imports: {len(failed)}")
    
    if failed:
        print("\nFailed packages:")
        for package, error in failed:
            print(f"  - {package}")
        return False
    else:
        print("\n🎉 All packages imported successfully!")
        return True

if __name__ == "__main__":
    test_imports()

