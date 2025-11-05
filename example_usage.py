"""
Example Usage: LLM Response Evaluator for Educational Content
Demonstrates practical applications for quality assurance of AI-generated educational responses
"""

from llm_response_evaluator import EducationalResponseEvaluator
import json
from datetime import datetime


def example_1_single_evaluation():
    """Example 1: Evaluate a single response"""
    print("=" * 60)
    print("Example 1: Single Response Evaluation")
    print("=" * 60)
    
    evaluator = EducationalResponseEvaluator(grade_level="6-8")
    
    prompt = "Explain the water cycle in simple terms"
    response = """The water cycle is the continuous movement of water on Earth. 

    It begins when the sun heats water in oceans, lakes, and rivers, causing it to 
    evaporate and turn into water vapor. This vapor rises into the atmosphere where 
    it cools and condenses to form clouds.

    When clouds become heavy with water droplets, precipitation occurs as rain, snow, 
    or hail. This water falls back to Earth's surface, where it flows into rivers and 
    streams, eventually returning to the ocean.

    Some water also seeps into the ground, becoming groundwater that plants use or 
    that eventually flows back to water bodies. This cycle repeats continuously, 
    recycling Earth's water supply."""
    
    expected_topics = ["evaporation", "condensation", "precipitation", "collection"]
    
    result = evaluator.evaluate_response(
        prompt=prompt,
        response=response,
        expected_topics=expected_topics,
        context={"subject": "earth_science"}
    )
    
    print(f"\nPrompt: {prompt}")
    print(f"\nEvaluation Results:")
    print(f"  Overall Score: {result.overall_score}/1.0 ({result.quality_level.value})")
    print(f"  Relevance: {result.relevance_score:.2%}")
    print(f"  Completeness: {result.completeness_score:.2%}")
    print(f"  Educational Value: {result.educational_value:.2%}")
    print(f"  Safety: {result.safety_level.value}")
    
    if result.feedback:
        print("\nFeedback for improvement:")
        for feedback in result.feedback:
            print(f"  • {feedback}")


def example_2_comparative_evaluation():
    """Example 2: Compare multiple responses to same prompt"""
    print("\n" + "=" * 60)
    print("Example 2: Comparative Response Evaluation")
    print("=" * 60)
    
    evaluator = EducationalResponseEvaluator(grade_level="9-12")
    
    prompt = "What causes seasons on Earth?"
    
    responses = {
        "Response A (Brief)": """Seasons are caused by Earth's tilt. As Earth orbits the sun, 
        different parts receive more direct sunlight at different times of the year.""",
        
        "Response B (Detailed)": """Earth experiences seasons due to its axial tilt of 
        approximately 23.5 degrees relative to its orbital plane around the sun.

        During summer in the Northern Hemisphere (June-August), the North Pole tilts toward 
        the sun, causing:
        - More direct sunlight hitting the Northern Hemisphere
        - Longer daylight hours
        - Higher sun angle in the sky
        - More concentrated solar energy per unit area

        Simultaneously, the Southern Hemisphere experiences winter with opposite conditions.

        This pattern reverses six months later when Earth is on the opposite side of its 
        orbit. The tilt remains constant, but now the South Pole tilts toward the sun.

        Common misconception: Seasons are NOT caused by Earth's distance from the sun. 
        In fact, Earth is closest to the sun in January when it's winter in the Northern 
        Hemisphere.""",
        
        "Response C (Incorrect)": """Seasons happen because Earth moves closer to and farther 
        from the sun during its orbit. When we're closer, it's summer, and when we're farther 
        away, it's winter. This distance changes throughout the year."""
    }
    
    print(f"\nPrompt: {prompt}\n")
    
    comparison_results = []
    for name, response in responses.items():
        result = evaluator.evaluate_response(
            prompt=prompt,
            response=response,
            expected_topics=["tilt", "orbit", "sunlight", "hemisphere"],
            context={"subject": "astronomy"}
        )
        
        comparison_results.append({
            "name": name,
            "score": result.overall_score,
            "quality": result.quality_level.value,
            "accuracy": result.accuracy_indicators
        })
        
        print(f"{name}:")
        print(f"  Score: {result.overall_score:.2f} ({result.quality_level.value})")
        print(f"  Accuracy Indicators: {result.accuracy_indicators:.2%}")
        
        if result.patterns_detected:
            print(f"  Patterns: {', '.join(result.patterns_detected)}")
    
    # Identify best response
    best = max(comparison_results, key=lambda x: x["score"])
    print(f"\n✅ Best Response: {best['name']} with score {best['score']:.2f}")


def example_3_pattern_analysis():
    """Example 3: Analyze patterns across multiple responses"""
    print("\n" + "=" * 60)
    print("Example 3: Pattern Analysis Across Multiple Responses")
    print("=" * 60)
    
    evaluator = EducationalResponseEvaluator(grade_level="general")
    
    # Simulate multiple responses with known issues
    test_cases = [
        {
            "prompt": "What is 5 + 3?",
            "response": "I understand you want to know about addition! The answer is 8."
        },
        {
            "prompt": "Define photosynthesis",
            "response": "I understand you're asking about photosynthesis. It's how plants make food using sunlight."
        },
        {
            "prompt": "Explain gravity",
            "response": "Gravity pulls things down!!! It's so amazing!!! Everything falls to Earth!!!"
        },
        {
            "prompt": "What's the capital of France?",
            "response": "paris"  # Lowercase start
        },
        {
            "prompt": "Describe the solar system",
            "response": "The solar system has eight planets. The solar system has eight planets. They orbit the sun."
        }
    ]
    
    results = evaluator.batch_evaluate(test_cases)
    
    print("\nPattern Analysis Results:")
    print(f"Total Responses Analyzed: {results['total_evaluated']}")
    print(f"Average Quality Score: {results['average_score']:.2f}/1.0")
    
    print("\nDetected Patterns (frequency):")
    for pattern, count in results['common_patterns']:
        percentage = (count / results['total_evaluated']) * 100
        print(f"  • {pattern}: {count} times ({percentage:.0f}%)")
    
    print("\nQuality Distribution:")
    for level, count in results['quality_distribution'].items():
        print(f"  • {level}: {count} responses")


def example_4_feedback_generation():
    """Example 4: Generate actionable feedback for teachers"""
    print("\n" + "=" * 60)
    print("Example 4: Generating Actionable Feedback")
    print("=" * 60)
    
    evaluator = EducationalResponseEvaluator(grade_level="K-5")
    
    # Problematic response that needs feedback
    prompt = "How do I teach counting to kindergarten students?"
    response = """Teaching counting is easy. Just tell the students the numbers from 1 to 100 
    and make them memorize everything. Use complex mathematical concepts to explain why numbers 
    exist. You might want to introduce algebra early."""
    
    result = evaluator.evaluate_response(
        prompt=prompt,
        response=response,
        expected_topics=["hands-on", "games", "visual", "practice", "fun"],
        context={"subject": "math", "audience": "teachers"}
    )
    
    print(f"\nPrompt: {prompt}")
    print(f"\nResponse Quality: {result.quality_level.value}")
    print(f"Overall Score: {result.overall_score:.2f}/1.0")
    
    print("\n🔍 Detailed Feedback:")
    for i, feedback in enumerate(result.feedback, 1):
        print(f"  {i}. {feedback}")
    
    print("\n💡 Suggested Improvements:")
    print("  • Include age-appropriate teaching methods")
    print("  • Add hands-on activities and games")
    print("  • Focus on visual and tangible learning tools")
    print("  • Ensure content matches K-5 complexity level")


def example_5_export_report():
    """Example 5: Generate and export evaluation reports"""
    print("\n" + "=" * 60)
    print("Example 5: Generating Evaluation Reports")
    print("=" * 60)
    
    evaluator = EducationalResponseEvaluator(grade_level="6-8")
    
    # Multiple test cases for report
    test_cases = [
        {
            "prompt": "What is democracy?",
            "response": "Democracy is a system of government where citizens vote to elect their leaders and have a say in how they are governed. Key features include free elections, individual rights, and rule of law.",
            "expected_topics": ["voting", "citizens", "government", "elections"]
        },
        {
            "prompt": "Explain fractions",
            "response": "Fractions represent parts of a whole. For example, 1/2 means one part out of two equal parts. You can add, subtract, multiply, and divide fractions using specific rules.",
            "expected_topics": ["numerator", "denominator", "parts", "whole"]
        },
        {
            "prompt": "Describe the human digestive system",
            "response": "The digestive system breaks down food into nutrients. It includes the mouth, esophagus, stomach, small intestine, large intestine, and other organs. Each part has a specific function in processing food.",
            "expected_topics": ["stomach", "intestines", "enzymes", "nutrients"]
        }
    ]
    
    # Run batch evaluation
    batch_results = evaluator.batch_evaluate(test_cases)
    
    # Export as JSON
    json_report = evaluator.export_evaluation_report(batch_results, format="json")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"evaluation_report_{timestamp}.json"
    
    with open(filename, "w") as f:
        f.write(json_report)
    
    print(f"\n📊 Report Summary:")
    print(f"  • Total Evaluations: {batch_results['total_evaluated']}")
    print(f"  • Average Score: {batch_results['average_score']:.2%}")
    print(f"  • Report saved to: {filename}")
    
    # Export as Markdown
    markdown_report = evaluator.export_evaluation_report(batch_results, format="markdown")
    md_filename = f"evaluation_report_{timestamp}.md"
    
    with open(md_filename, "w") as f:
        f.write(markdown_report)
    
    print(f"  • Markdown report saved to: {md_filename}")


def main():
    """Run all examples"""
    print("\n🚀 LLM Response Evaluator - Example Usage Demonstrations\n")
    
    examples = [
        example_1_single_evaluation,
        example_2_comparative_evaluation,
        example_3_pattern_analysis,
        example_4_feedback_generation,
        example_5_export_report
    ]
    
    for example in examples:
        example()
        input("\nPress Enter to continue to next example...")
    
    print("\n✅ All examples completed successfully!")
    print("\n💡 These examples demonstrate:")
    print("  • Single response evaluation")
    print("  • Comparative analysis")
    print("  • Pattern detection")
    print("  • Feedback generation")
    print("  • Report creation")
    print("\nPerfect for LLM quality assurance in educational contexts!")


if __name__ == "__main__":
    main()
