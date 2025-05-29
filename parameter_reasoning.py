

def test_parameter_conflicts():
    """My basic test - do we understand parameter conflicts?"""
    
    # Test configuration from user (simulating what they might try)
    user_config = {
        'sched.vcpu0.affinity': '0,1',
        'sched.vcpu1.affinity': '2,3', 
        'sched.numa.nodeAffinity': '0',  # CONFLICT! This conflicts with vcpu affinity
        'sched.mem.ballooning': '1'      # BAD for SAP HANA!
    }
    
    print("User wants to configure:")
    for param, value in user_config.items():
        print(f"  {param} = {value}")
    
    # Step 1: Check for known conflicts (why I chose simple rules - reliable)
    conflicts = []
    
    # Test the specific conflict mentioned in assignment
    has_vcpu = any('vcpu' in param for param in user_config.keys())
    has_numa = any('numa' in param for param in user_config.keys())
    
    if has_vcpu and has_numa:
        conflicts.append("CONFLICT: sched.vcpu*.affinity and sched.numa.nodeAffinity are mutually exclusive")
    
    # Test SAP HANA specific requirements
    if user_config.get('sched.mem.ballooning') != '0':
        conflicts.append("ERROR: sched.mem.ballooning must be 0 for SAP HANA")
    
    # Step 2: Report what I found
    print(f"\n🚨 Conflicts detected: {len(conflicts)}")
    for conflict in conflicts:
        print(f"  - {conflict}")
    
    # Step 3: Simple recommendation logic
    print(f"\n💡 My recommendation:")
    if has_vcpu and has_numa:
        print("  - Remove vCPU affinity settings, keep NUMA affinity for SAP HANA")
    print("  - Set sched.mem.ballooning = 0 (required for SAP HANA)")
    
    return len(conflicts)

def test_step_by_step_reasoning():
    """Test: Can I do chain of thought for system recommendations?"""
    
    # System specs (simulating user input)
    system_specs = {'cpu_count': 16, 'memory_gb': 128, 'workload': 'sap_hana_production'}
    
    print(f"\n🤔 Step-by-step reasoning for {system_specs}:")
    
    # Step 1: Analyze system size
    if system_specs['cpu_count'] >= 16:
        print("  1. Large system (16+ CPUs) → NUMA optimization recommended")
        recommendation = 'numa_affinity'
    else:
        print("  1. Small system (<16 CPUs) → vCPU affinity sufficient") 
        recommendation = 'vcpu_affinity'
    
    # Step 2: Workload consideration
    if 'sap_hana' in system_specs['workload']:
        print("  2. SAP HANA workload → Disable memory ballooning")
        print("  3. SAP HANA production → Prefer NUMA for memory locality")
        recommendation = 'numa_affinity'
    
    # Step 3: Final recommendation
    print(f"\n✅ Final recommendation: Use {recommendation}")
    
    return recommendation

if __name__ == "__main__":
    print("=== Testing Parameter Reasoning ===")
    conflict_count = test_parameter_conflicts()
    recommendation = test_step_by_step_reasoning()
    print(f"\nResult: Found {conflict_count} conflicts, recommended {recommendation}")
    
    
    