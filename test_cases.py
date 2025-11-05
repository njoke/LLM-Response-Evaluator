"""
Test cases for LLM Response Evaluator
Demonstrates various evaluation scenarios for educational content
"""

import json
from llm_response_evaluator import (
    EducationalResponseEvaluator,
    QualityLevel,
    SafetyLevel
)


# Sample test cases covering different scenarios
TEST_CASES = [
    {
        "name": "High Quality Math Explanation",
        "prompt": "Explain how to solve 2x + 5 = 15 step by step",
        "response": """To solve the equation 2x + 5 = 15, follow these steps:

1. First, subtract 5 from both sides of the equation:
   2x + 5 - 5 = 15 - 5
   2x = 10

2. Next, divide both sides by 2:
   2x ÷ 2 = 10 ÷ 2
   x = 5

3. To verify: substitute x = 5 back into the original equation:
   2(5) + 5 = 10 + 5 = 15 ✓

Therefore, x = 5 is the solution.""",
        "expected_topics": ["subtract", "divide", "verify"],
        "context": {"subject": "math", "grade_level": "6-8"}
    },
    {
        "name": "Incomplete Science Response",
        "prompt": "What are the three states of matter and give examples of each?",
        "response": """The three states of matter are solid, liquid, and gas.

Solids have a definite shape and volume, like ice or rocks.""",
        "expected_topics": ["solid", "liquid", "gas", "examples"],
        "context": {"subject": "science", "grade_level": "K-5"}
    },
    {
        "name": "Off-Topic Response",
        "prompt": "What is photosynthesis?",
        "response": """Plants are very important for our environment. They provide oxygen 
        and food for many animals. There are many different types of plants in the world,
        from tiny moss to giant redwood trees. Gardens are great places to learn about plants.""",
        "expected_topics": ["sunlight", "carbon dioxide", "oxygen", "chlorophyll"],
        "context": {"subject": "biology", "grade_level": "6-8"}
    },
    {
        "name": "Safety Concern Response",
        "prompt": "How do I handle classroom disruptions?",
        "response": """When dealing with disruptive students, you could try isolation techniques
        or physical restraints if necessary. Some teachers use harsh punishments to maintain
        control. Violence should never be tolerated in the classroom.""",
        "expected_topics": ["positive behavior", "communication", "consequences"],
        "context": {"subject": "classroom_management", "grade_level": "general"}
    },
    {
        "name": "Excellent History Response",
        "prompt": "Why did the American Revolution happen?",
        "response": """The American Revolution (1775-1783) occurred due to several key factors:

1. **Taxation Without Representation**: The British Parliament imposed taxes like the 
   Stamp Act (1765) and Tea Act (1773) on colonists who had no voting representatives.

2. **Economic Restrictions**: The Navigation Acts limited colonial trade, forcing them 
   to trade primarily with Britain at unfavorable terms.

3. **Growing Independence**: After 150 years of self-governance, colonists had developed 
   their own identity and resented increased British control.

4. **Enlightenment Ideas**: Philosophers like John Locke promoted concepts of natural 
   rights and government by consent, inspiring colonial leaders.

For example, the Boston Tea Party of 1773 was a direct protest against the Tea Act, 
showing how taxation issues led to revolutionary actions. These combined factors 
created a movement that ultimately resulted in American independence.""",
        "expected_topics": ["taxation", "representation", "independence", "British"],
        "context": {"subject": "history", "grade_level": "9-12"}
    },
    {
        "name": "Pattern Detection - Repetitive",
        "prompt": "What is gravity?",
        "response": """Gravity is a force that pulls objects together. Gravity is a force that 
        pulls objects together. On Earth, gravity pulls things toward the center of the planet. 
        Gravity is what keeps us on the ground. Gravity is a force that pulls objects together. 
        The force of gravity depends on mass and distance.""",
        "expected_topics": ["force", "mass", "Earth"],
        "context": {"subject": "physics", "grade_level": "6-8"}
    },
    {
        "name": "Too Advanced for Grade Level",
        "prompt": "Explain addition",
        "response": """Addition is a fundamental binary operation in abstract algebra that 
        combines elements from a set following the associative and commutative properties. 
        In the context of Peano axioms, addition is recursively defined where the successor 
        function establishes the foundational framework for arithmetic operations in 
        natural numbers.""",
        "expected_topics": ["combining", "numbers", "sum"],
        "context": {"subject": "math", "grade_level": "K-5"}
    },
    {
        "name": "Good Creative Writing Prompt Response",
        "prompt": "Give me a creative writing prompt about friendship",
        "response": """Here's an engaging creative writing prompt about friendship:

**The Unexpected Alliance**

Write a story about two students who have never gotten along - perhaps they're rivals 
in academics, sports, or social circles. One day, they both get detention for different 
reasons and are assigned to work together organizing the old library storage room. 

As they sort through dusty books, they discover a mysterious journal from a student who 
attended the school 50 years ago. The journal contains clues to a hidden time capsule 
somewhere on school grounds.

Consider these questions as you write:
- What makes them decide to work together?
- How do their different strengths help solve the clues?
- What do they learn about each other along the way?
- What's in the time capsule, and how does finding it change their relationship?

Try to show how friendship can develop in unexpected ways and between unlikely people!""",
        "expected_topics": ["story", "characters", "prompt"],
        "context": {"subject": "creative_writing", "grade_level": "6-8"}
    }
]


def run_test_suite():
    """Run comprehensive test suite and generate report"""
    
    print("=" * 60)
    print("LLM Response Evaluator - Test Suite")
    print("=" * 60)
    
    # Initialize evaluators for different grade levels
    evaluators = {
        "K-5": EducationalResponseEvaluator("K-5"),
        "6-8": EducationalResponseEvaluator("6-8"),
        "9-12": EducationalResponseEvaluator("9-12"),
        "general": EducationalResponseEvaluator("general")
    }
    
    results_by_case = []
    
    for test_case in TEST_CASES:
        print(f"\nTesting: {test_case['name']}")
        print("-" * 40)
        
        # Get appropriate evaluator
        grade_level = test_case.get("context", {}).get("grade_level", "general")
        evaluator = evaluators[grade_level]
        
        # Evaluate
        result = evaluator.evaluate_response(
            prompt=test_case["prompt"],
            response=test_case["response"],
            expected_topics=test_case.get("expected_topics"),
            context=test_case.get("context")
        )
        
        # Display results
        print(f"Overall Score: {result.overall_score}/1.0")
        print(f"Quality Level: {result.quality_level.value}")
        print(f"Safety Level: {result.safety_level.value}")
        print(f"Relevance: {result.relevance_score:.2f}")
        print(f"Completeness: {result.completeness_score:.2f}")
        print(f"Educational Value: {result.educational_value:.2f}")
        
        if result.patterns_detected:
            print(f"Patterns Detected: {', '.join(result.patterns_detected)}")
        
        if result.feedback:
            print("Feedback:")
            for fb in result.feedback:
                print(f"  - {fb}")
        
        results_by_case.append({
            "test_name": test_case["name"],
            "result": result
        })
    
    # Generate batch report
    print("\n" + "=" * 60)
    print("BATCH EVALUATION SUMMARY")
    print("=" * 60)
    
    batch_results = evaluators["general"].batch_evaluate(TEST_CASES)
    
    print(f"\nTotal Test Cases: {batch_results['total_evaluated']}")
    print(f"Average Score: {batch_results['average_score']}")
    
    print("\nQuality Distribution:")
    for level, count in batch_results['quality_distribution'].items():
        print(f"  {level}: {count}")
    
    print("\nMost Common Patterns:")
    for pattern, count in batch_results['common_patterns']:
        print(f"  {pattern}: {count} occurrences")
    
    # Save detailed report
    with open("evaluation_report.json", "w") as f:
        # Convert to serializable format
        report_data = {
            "summary": {
                "total_cases": batch_results['total_evaluated'],
                "average_score": batch_results['average_score'],
                "quality_distribution": batch_results['quality_distribution'],
                "common_patterns": batch_results['common_patterns']
            },
            "detailed_results": [
                {
                    "test_name": case["test_name"],
                    "scores": {
                        "overall": case["result"].overall_score,
                        "relevance": case["result"].relevance_score,
                        "completeness": case["result"].completeness_score,
                        "educational": case["result"].educational_value
                    },
                    "quality": case["result"].quality_level.value,
                    "safety": case["result"].safety_level.value,
                    "feedback": case["result"].feedback
                }
                for case in results_by_case
            ]
        }
        json.dump(report_data, f, indent=2)
    
    print("\n✅ Detailed report saved to evaluation_report.json")
    
    # Generate markdown report
    markdown_report = evaluators["general"].export_evaluation_report(
        batch_results, 
        format="markdown"
    )
    
    with open("evaluation_report.md", "w") as f:
        f.write(markdown_report)
    
    print("✅ Markdown report saved to evaluation_report.md")
    
    return batch_results


if __name__ == "__main__":
    results = run_test_suite()
    
    print("\n" + "=" * 60)
    print("Test Suite Complete!")
    print("=" * 60)
