import requests
import time

# Define MCP server endpoints
servers = {
    "memory": "http://localhost:9100/v1/meta",
    "github": "http://localhost:9101/",
    "filesystem": "http://localhost:9102/",
    "supabase": "http://localhost:9103/",
    "obsidian": "http://localhost:9104/",
    "zotero": "http://localhost:9107/",
    "docgen": "http://localhost:9105/",
    "hugo": "http://localhost:9106/",
    "ollama": "http://localhost:9108/",
    "fabric": "http://localhost:9109/"
}

def test_server_reachability():
    print("\n--- Testing MCP Server Reachability ---")
    for name, url in servers.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"[SUCCESS] {name} ({url}) is reachable.")
            else:
                print(f"[FAILURE] {name} ({url}) returned status code {response.status_code}.")
        except requests.exceptions.ConnectionError:
            print(f"[FAILURE] {name} ({url}) is not reachable. Connection refused.")
        except requests.exceptions.Timeout:
            print(f"[FAILURE] {name} ({url}) timed out.")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred for {name} ({url}): {e}")

if __name__ == "__main__":
    print("Starting MCP server tests...")
    # Give some time for Docker containers to start up
    time.sleep(10)
    test_server_reachability()
    print("MCP server tests finished.")
