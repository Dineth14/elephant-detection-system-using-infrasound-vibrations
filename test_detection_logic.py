#!/usr/bin/env python3
"""
Simple test to validate detection logic without GUI window
"""

import sys
import os
import time

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class MockDetectionTest:
    def __init__(self):
        # Detection display timer (5-second intervals)
        self.detection_timer_start = 0
        self.detection_timer_duration = 5.0  # 5 seconds
        self.last_detection_state = "no_elephant"
        self.detection_locked = False
        
        self.current_classification = "not_elephant"
        self.current_confidence = 0.0
        
    def update_detection_display(self):
        """Update the detection display with 5-second persistence"""
        current_time = time.time()
        
        # Determine current detection state
        if self.current_classification == "elephant":
            if self.current_confidence > 0.5:  # Lowered threshold for better detection
                new_detection_state = "elephant_high"
            elif self.current_confidence > 0.3:
                new_detection_state = "elephant_medium"
            else:
                new_detection_state = "elephant_low"
        else:
            new_detection_state = "no_elephant"
        
        print(f"🔍 Current state: {new_detection_state}, Locked: {self.detection_locked}")
        
        # Check if we need to start a new 5-second detection period
        if new_detection_state != "no_elephant" and (not self.detection_locked or 
            new_detection_state != self.last_detection_state):
            # Start new 5-second detection period
            self.detection_timer_start = current_time
            self.detection_locked = True
            self.last_detection_state = new_detection_state
            
            if new_detection_state == "elephant_high":
                print("🐘 ELEPHANT DETECTED! 🚨 (RED BACKGROUND)")
            elif new_detection_state == "elephant_medium":
                print("🐘 Possible Elephant (ORANGE BACKGROUND)")
            else:
                print("🤔 Elephant (Low Confidence) (GRAY BACKGROUND)")
        
        # Check if 5-second period has elapsed
        elif self.detection_locked:
            elapsed = current_time - self.detection_timer_start
            remaining = max(0, self.detection_timer_duration - elapsed)
            print(f"⏱️ Detection active: {remaining:.1f}s remaining")
            
            if elapsed >= self.detection_timer_duration:
                # 5-second period finished, check current state
                self.detection_locked = False
                if new_detection_state == "no_elephant":
                    print("✅ No Elephant (GREEN BACKGROUND)")
                    self.last_detection_state = "no_elephant"
                else:
                    # Continue with current detection if still active
                    self.detection_timer_start = current_time
                    self.detection_locked = True
                    self.last_detection_state = new_detection_state
                    print("🔄 Detection continues...")
        
        # If no detection lock, show current state immediately
        elif not self.detection_locked and new_detection_state == "no_elephant":
            print("✅ No Elephant (GREEN BACKGROUND)")
            self.last_detection_state = "no_elephant"

def test_detection_logic():
    print("🧪 Testing Elephant Detection Logic")
    print("=" * 50)
    
    tester = MockDetectionTest()
    
    # Test 1: Simulate elephant detection
    print("\n📡 Test 1: Simulating elephant detection (confidence 0.85)")
    tester.current_classification = "elephant"
    tester.current_confidence = 0.85
    tester.update_detection_display()
    
    # Test 2: Wait 2 seconds and update again
    print("\n⏳ Waiting 2 seconds...")
    time.sleep(2)
    tester.update_detection_display()
    
    # Test 3: Change to no elephant while still in detection period
    print("\n📡 Test 3: Change to no elephant (should still show detection)")
    tester.current_classification = "not_elephant"
    tester.current_confidence = 0.1
    tester.update_detection_display()
    
    # Test 4: Wait another 4 seconds to complete the 5-second period
    print("\n⏳ Waiting 4 more seconds to complete 5-second period...")
    time.sleep(4)
    tester.update_detection_display()
    
    # Test 5: Now it should show no elephant
    print("\n📡 Test 5: Final state check")
    tester.update_detection_display()
    
    print("\n✅ Test completed! The logic should work correctly.")
    print("📝 Expected behavior:")
    print("   - Shows elephant detection immediately")
    print("   - Maintains detection for 5 seconds even if classification changes")
    print("   - Returns to 'No Elephant' after 5 seconds if no new detection")

if __name__ == "__main__":
    test_detection_logic()