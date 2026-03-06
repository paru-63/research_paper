"""
Neo4j Aura Connection Tester
This will help diagnose your connection issue
"""

print("=" * 80)
print("NEO4J AURA CONNECTION DIAGNOSTIC")
print("=" * 80)

# Step 1: Check Neo4j driver
print("\n1️⃣ Checking Neo4j driver installation...")
try:
    import neo4j
    print(f"✅ Neo4j driver installed (version {neo4j.__version__})")
except ImportError:
    print("❌ Neo4j driver NOT installed!")
    print("   Fix: pip install neo4j")
    exit()

# Step 2: Get connection details
print("\n2️⃣ Please provide your Aura connection details:")
print("   (You can find these in your Neo4j Aura console)")
print()

# Your database details
uri = input("URI (press Enter for default): ").strip()
if not uri:
    uri = "neo4j+s://b83346a2.databases.neo4j.io"
    print(f"   Using: {uri}")

user = input("Username (press Enter for 'neo4j'): ").strip()
if not user:
    user = "neo4j"
    print(f"   Using: {user}")

password = input("Password: ").strip()

if not password:
    print("❌ Password is required!")
    exit()

# Step 3: Test different connection methods
print("\n3️⃣ Testing connection methods...")

from neo4j import GraphDatabase

# Method 1: Standard connection
print("\n   Testing: neo4j+s:// (Aura default)")
try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        test_result = result.single()
        if test_result and test_result['test'] == 1:
            print("   ✅ SUCCESS with neo4j+s://")
            
            # Get database info
            result = session.run("CALL dbms.components() YIELD name, versions RETURN name, versions[0] as version")
            for record in result:
                print(f"      {record['name']}: {record['version']}")
            
            # Count existing data
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()['count']
            print(f"      Current nodes in database: {count}")
            
    driver.close()
    print("\n🎉 CONNECTION SUCCESSFUL!")
    print("   You can now run: python neo4j_aura_fixed.py")
    
except Exception as e:
    print(f"   ❌ FAILED: {e}")
    print("\n   Trying alternative methods...")
    
    # Method 2: Try with verify_connectivity=False
    print("\n   Testing: Connection without connectivity check")
    try:
        driver = GraphDatabase.driver(
            uri, 
            auth=(user, password),
            encrypted=True,
            trust=neo4j.TRUST_SYSTEM_CA_SIGNED_CERTIFICATES
        )
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            result.single()
            print("   ✅ SUCCESS with alternative method")
        driver.close()
        
    except Exception as e2:
        print(f"   ❌ FAILED: {e2}")

# Step 4: Common issues checklist
print("\n4️⃣ TROUBLESHOOTING CHECKLIST:")
print()
print("   Check these in your Neo4j Aura Console (https://console.neo4j.io):")
print()
print("   [ ] Is your instance RUNNING? (should show green status)")
print("   [ ] Is this the correct instance ID: b83346a2?")
print("   [ ] Did you copy the password correctly?")
print("   [ ] Is your instance paused or stopped?")
print()
print("   Check your local setup:")
print("   [ ] Are you connected to the internet?")
print("   [ ] Is any firewall blocking port 7687?")
print("   [ ] Are you on a corporate/school network with restrictions?")
print()

# Step 5: Provide specific solutions
print("\n5️⃣ COMMON SOLUTIONS:")
print()
print("   Solution 1: Reset your Aura password")
print("   - Go to https://console.neo4j.io")
print("   - Click on instance b83346a2")
print("   - Click 'Generate new password'")
print("   - Copy the new password")
print("   - Try connecting again")
print()
print("   Solution 2: Check instance status")
print("   - Go to https://console.neo4j.io")
print("   - Make sure instance shows GREEN (running)")
print("   - If it's paused/stopped, click 'Resume' or 'Start'")
print()
print("   Solution 3: Verify connection details")
print("   Your connection details should be:")
print(f"   URI: neo4j+s://b83346a2.databases.neo4j.io")
print(f"   Username: neo4j")
print(f"   Password: [your Aura password]")
print()
print("   Solution 4: Network issues")
print("   - Try from a different network")
print("   - Disable VPN if using one")
print("   - Check with your network admin")
print()

print("=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)