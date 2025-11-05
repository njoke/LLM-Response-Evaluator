"""
LLM Response Evaluator for Educational Content
A comprehensive framework for evaluating AI-generated educational responses
Author: [Your Name]
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import statistics


class QualityLevel(Enum):
    """Quality levels for response evaluation"""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    NEEDS_IMPROVEMENT = "needs_improvement"
    UNACCEPTABLE = "unacceptable"


class SafetyLevel(Enum):
    """Safety classifications for educational content"""
    SAFE = "safe"
    REVIEW_NEEDED = "review_needed"
    UNSAFE = "unsafe"


@dataclass
class EvaluationResult:
    """Structured result from response evaluation"""
    overall_score: float
    quality_level: QualityLevel
    safety_level: SafetyLevel
    relevance_score: float
    completeness_score: float
    accuracy_indicators: float
    educational_value: float
    age_appropriateness: bool
    feedback: List[str]
    patterns_detected: List[str]
    metadata: Dict


class EducationalResponseEvaluator:
    """
    Evaluates LLM responses for quality, safety, and educational value.
    Designed for K-12 educational content assessment.
    """
    
    def __init__(self, grade_level: str = "general"):
        """
        Initialize evaluator with configuration
        
        Args:
            grade_level: Target grade level (K-5, 6-8, 9-12, or general)
        """
        self.grade_level = grade_level
        self.safety_keywords = self._load_safety_keywords()
        self.educational_rubric = self._load_educational_rubric()
        self.evaluation_history = []
        
    def _load_safety_keywords(self) -> Dict[str, List[str]]:
        """Load keywords for safety checking"""
        return {
            "inappropriate": ["violence", "explicit", "inappropriate", "harmful"],
            "sensitive": ["politics", "religion", "controversial"],
            "medical": ["diagnosis", "prescription", "medical advice"],
            "personal": ["personal information", "private", "address", "phone"]
        }
    
    def _load_educational_rubric(self) -> Dict[str, float]:
        """Load scoring rubric for educational content"""
        return {
            "has_explanation": 0.2,
            "has_examples": 0.15,
            "structured_response": 0.15,
            "appropriate_complexity": 0.2,
            "encourages_learning": 0.15,
            "accurate_information": 0.15
        }
    
    def evaluate_response(
        self, 
        prompt: str, 
        response: str, 
        expected_topics: List[str] = None,
        context: Dict = None
    ) -> EvaluationResult:
        """
        Comprehensive evaluation of an LLM response
        
        Args:
            prompt: The original prompt/question
            response: The LLM's response
            expected_topics: Topics that should be covered
            context: Additional context (subject, grade level, etc.)
            
        Returns:
            EvaluationResult with detailed scoring and feedback
        """
        feedback = []
        patterns = []
        
        # Core evaluations
        relevance = self._evaluate_relevance(prompt, response)
        completeness = self._evaluate_completeness(response, expected_topics)
        safety = self._evaluate_safety(response)
        accuracy = self._evaluate_accuracy_indicators(response)
        educational = self._evaluate_educational_value(response, context)
        age_appropriate = self._check_age_appropriateness(response)
        
        # Pattern detection
        patterns = self._detect_patterns(response)
        
        # Calculate overall score
        scores = [relevance, completeness, accuracy, educational]
        overall_score = statistics.mean(scores)
        
        # Determine quality level
        quality_level = self._determine_quality_level(overall_score)
        
        # Generate feedback
        feedback = self._generate_feedback(
            relevance, completeness, safety, accuracy, educational, patterns
        )
        
        return EvaluationResult(
            overall_score=round(overall_score, 2),
            quality_level=quality_level,
            safety_level=safety,
            relevance_score=relevance,
            completeness_score=completeness,
            accuracy_indicators=accuracy,
            educational_value=educational,
            age_appropriateness=age_appropriate,
            feedback=feedback,
            patterns_detected=patterns,
            metadata={
                "prompt_length": len(prompt.split()),
                "response_length": len(response.split()),
                "grade_level": self.grade_level
            }
        )
    
    def _evaluate_relevance(self, prompt: str, response: str) -> float:
        """
        Evaluate how well the response addresses the prompt
        
        Returns:
            Score between 0 and 1
        """
        score = 0.0
        prompt_keywords = set(prompt.lower().split())
        response_lower = response.lower()
        
        # Check keyword presence
        keyword_matches = sum(1 for keyword in prompt_keywords 
                             if keyword in response_lower)
        if prompt_keywords:
            score += (keyword_matches / len(prompt_keywords)) * 0.5
        
        # Check if response directly addresses the question
        question_types = {
            "what": ["is", "are", "means", "defined"],
            "how": ["by", "through", "using", "with", "steps"],
            "why": ["because", "reason", "due to", "since"],
            "when": ["time", "date", "period", "after", "before"],
            "where": ["location", "place", "at", "in"]
        }
        
        for q_type, indicators in question_types.items():
            if q_type in prompt.lower():
                if any(indicator in response_lower for indicator in indicators):
                    score += 0.3
                break
        
        # Check response structure
        if response.strip() and len(response.split()) > 10:
            score += 0.2
            
        return min(score, 1.0)
    
    def _evaluate_completeness(
        self, 
        response: str, 
        expected_topics: List[str] = None
    ) -> float:
        """
        Evaluate if response covers all expected topics
        
        Returns:
            Score between 0 and 1
        """
        if not expected_topics:
            # Basic completeness check
            sentences = response.split('.')
            if len(sentences) < 2:
                return 0.3
            elif len(sentences) < 4:
                return 0.6
            else:
                return 0.9
        
        # Check coverage of expected topics
        response_lower = response.lower()
        covered = sum(1 for topic in expected_topics 
                     if topic.lower() in response_lower)
        
        return covered / len(expected_topics) if expected_topics else 0.5
    
    def _evaluate_safety(self, response: str) -> SafetyLevel:
        """
        Evaluate response for safety in educational context
        
        Returns:
            SafetyLevel enum
        """
        response_lower = response.lower()
        
        # Check for unsafe content
        for keyword in self.safety_keywords["inappropriate"]:
            if keyword in response_lower:
                return SafetyLevel.UNSAFE
        
        # Check for sensitive content
        sensitive_count = sum(
            1 for keyword in self.safety_keywords["sensitive"]
            if keyword in response_lower
        )
        
        if sensitive_count > 2:
            return SafetyLevel.REVIEW_NEEDED
        
        # Check for medical/personal information
        for category in ["medical", "personal"]:
            if any(keyword in response_lower 
                  for keyword in self.safety_keywords[category]):
                return SafetyLevel.REVIEW_NEEDED
        
        return SafetyLevel.SAFE
    
    def _evaluate_accuracy_indicators(self, response: str) -> float:
        """
        Look for indicators of accuracy (not fact-checking, but patterns)
        
        Returns:
            Score between 0 and 1
        """
        score = 0.0
        
        # Positive indicators
        positive_patterns = [
            r'\b\d{4}\b',  # Years (suggests specific facts)
            r'\b\d+%\b',    # Percentages
            r'according to', # Attribution
            r'research shows',
            r'studies indicate',
            r'for example',
            r'specifically',
        ]
        
        for pattern in positive_patterns:
            if re.search(pattern, response.lower()):
                score += 0.15
        
        # Negative indicators
        negative_patterns = [
            r'maybe',
            r'might be',
            r'could be',
            r'i think',
            r'probably',
            r'guess'
        ]
        
        for pattern in negative_patterns:
            if re.search(pattern, response.lower()):
                score -= 0.1
        
        return max(0, min(score, 1.0))
    
    def _evaluate_educational_value(
        self, 
        response: str, 
        context: Dict = None
    ) -> float:
        """
        Evaluate the educational value of the response
        
        Returns:
            Score between 0 and 1
        """
        score = 0.0
        response_lower = response.lower()
        
        # Check against rubric
        if "because" in response_lower or "explain" in response_lower:
            score += self.educational_rubric["has_explanation"]
        
        if "example" in response_lower or "such as" in response_lower:
            score += self.educational_rubric["has_examples"]
        
        # Check structure (lists, steps, clear paragraphs)
        if re.search(r'\n\d+\.|\n-|\n\*', response) or response.count('\n') > 2:
            score += self.educational_rubric["structured_response"]
        
        # Check for encouraging language
        encouraging_phrases = ["you can", "try", "explore", "learn", "discover", "practice"]
        if any(phrase in response_lower for phrase in encouraging_phrases):
            score += self.educational_rubric["encourages_learning"]
        
        # Complexity check based on grade level
        avg_word_length = sum(len(word) for word in response.split()) / max(len(response.split()), 1)
        if self.grade_level == "K-5" and avg_word_length < 6:
            score += self.educational_rubric["appropriate_complexity"]
        elif self.grade_level in ["6-8", "9-12"] and 5 < avg_word_length < 8:
            score += self.educational_rubric["appropriate_complexity"]
        elif self.grade_level == "general":
            score += self.educational_rubric["appropriate_complexity"] * 0.5
        
        return min(score, 1.0)
    
    def _check_age_appropriateness(self, response: str) -> bool:
        """
        Check if content is appropriate for the grade level
        
        Returns:
            True if appropriate, False otherwise
        """
        if self.grade_level == "K-5":
            # Check for complex vocabulary
            complex_words = len([w for w in response.split() if len(w) > 10])
            if complex_words > 5:
                return False
                
        return True
    
    def _detect_patterns(self, response: str) -> List[str]:
        """
        Detect common patterns or issues in responses
        
        Returns:
            List of detected patterns
        """
        patterns = []
        
        # Check for common LLM patterns
        if response.startswith("I understand"):
            patterns.append("starts_with_acknowledgment")
        
        if response.count("!") > 3:
            patterns.append("excessive_enthusiasm")
        
        if "I cannot" in response or "I can't" in response:
            patterns.append("contains_refusal")
        
        if len(response.split('.')) > 10:
            patterns.append("very_long_response")
        elif len(response.split('.')) < 2:
            patterns.append("very_short_response")
        
        # Check for repetition
        sentences = response.split('.')
        if len(sentences) > len(set(sentences)) + 2:
            patterns.append("repetitive_content")
        
        # Check for formatting issues
        if response.count('\n\n') > 5:
            patterns.append("excessive_spacing")
        
        if not response[0].isupper():
            patterns.append("lowercase_start")
        
        return patterns
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """
        Determine quality level based on overall score
        
        Returns:
            QualityLevel enum
        """
        if score >= 0.9:
            return QualityLevel.EXCELLENT
        elif score >= 0.75:
            return QualityLevel.GOOD
        elif score >= 0.6:
            return QualityLevel.ACCEPTABLE
        elif score >= 0.4:
            return QualityLevel.NEEDS_IMPROVEMENT
        else:
            return QualityLevel.UNACCEPTABLE
    
    def _generate_feedback(
        self, 
        relevance: float,
        completeness: float,
        safety: SafetyLevel,
        accuracy: float,
        educational: float,
        patterns: List[str]
    ) -> List[str]:
        """
        Generate actionable feedback based on evaluation
        
        Returns:
            List of feedback items
        """
        feedback = []
        
        if relevance < 0.7:
            feedback.append("Response could be more directly relevant to the prompt")
        
        if completeness < 0.7:
            feedback.append("Response appears incomplete or missing expected content")
        
        if safety != SafetyLevel.SAFE:
            feedback.append(f"Safety review needed: {safety.value}")
        
        if accuracy < 0.5:
            feedback.append("Response lacks specific facts or attribution")
        
        if educational < 0.6:
            feedback.append("Could improve educational value with examples or clearer structure")
        
        if "repetitive_content" in patterns:
            feedback.append("Response contains repetitive content")
        
        if "very_short_response" in patterns:
            feedback.append("Response may be too brief for educational purposes")
        
        return feedback
    
    def batch_evaluate(
        self, 
        test_cases: List[Dict]
    ) -> Dict:
        """
        Evaluate multiple test cases and aggregate results
        
        Args:
            test_cases: List of dicts with 'prompt' and 'response' keys
            
        Returns:
            Aggregated results and patterns
        """
        results = []
        all_patterns = []
        quality_distribution = {level: 0 for level in QualityLevel}
        
        for case in test_cases:
            result = self.evaluate_response(
                case.get("prompt"),
                case.get("response"),
                case.get("expected_topics"),
                case.get("context")
            )
            results.append(result)
            all_patterns.extend(result.patterns_detected)
            quality_distribution[result.quality_level] += 1
        
        # Calculate aggregated metrics
        avg_score = statistics.mean([r.overall_score for r in results])
        pattern_frequency = {}
        for pattern in all_patterns:
            pattern_frequency[pattern] = pattern_frequency.get(pattern, 0) + 1
        
        return {
            "total_evaluated": len(test_cases),
            "average_score": round(avg_score, 2),
            "quality_distribution": {
                level.value: count 
                for level, count in quality_distribution.items()
            },
            "common_patterns": sorted(
                pattern_frequency.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],
            "detailed_results": results
        }
    
    def export_evaluation_report(
        self, 
        results: Dict,
        format: str = "json"
    ) -> str:
        """
        Export evaluation results in specified format
        
        Args:
            results: Results from batch_evaluate
            format: Output format (json, markdown, csv)
            
        Returns:
            Formatted report string
        """
        if format == "json":
            return json.dumps(results, indent=2, default=str)
        
        elif format == "markdown":
            report = "# LLM Response Evaluation Report\n\n"
            report += f"## Summary\n"
            report += f"- Total Evaluated: {results['total_evaluated']}\n"
            report += f"- Average Score: {results['average_score']}\n\n"
            
            report += "## Quality Distribution\n"
            for level, count in results['quality_distribution'].items():
                report += f"- {level}: {count}\n"
            
            report += "\n## Common Patterns\n"
            for pattern, count in results['common_patterns']:
                report += f"- {pattern}: {count} occurrences\n"
            
            return report
        
        else:
            raise ValueError(f"Unsupported format: {format}")
