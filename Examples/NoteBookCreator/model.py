"""Notebook content structure models"""

from __future__ import annotations

from typing import Optional, List, Literal, Dict, Union
from pydantic import BaseModel, ConfigDict


class BaseExample(BaseModel):
    """Fields shared by all question types."""
    model_config = ConfigDict(strict=False)
    
    # IDs identify individual fields and remain optional for backward compatibility.
    id: Optional[str] = None  # Unique ID, for example "example_abc123"
    question_id: Optional[str] = None  # ID for the question field
    question: str  # Question or example text (required)


class MultipleChoiceQuestion(BaseExample):
    """Multiple-choice question"""
    model_config = ConfigDict(strict=False)
    
    answer_id: Optional[str] = None  # ID for the answer field
    explanation_id: Optional[str] = None  # ID for the explanation field
    
    options: List[str]  # List of options (required, typically four)
    correct_answer: str  # Correct answer (required, e.g. "A", "B", "C", or "D")
    explanation: Optional[str] = None  # Explanation (optional)


class FillBlankQuestion(BaseExample):
    """Fill-in-the-blank question"""
    model_config = ConfigDict(strict=False)
    
    answer_id: Optional[str] = None  # ID for the answer field
    explanation_id: Optional[str] = None  # ID for the explanation field
    
    blanks: Dict[str, str]  # Mapping from placeholders to answers (required)
    # Example: {"[blank1]": "answer 1", "[blank2]": "answer 2"}
    # Keys must match the placeholders in question exactly.
    explanation: Optional[str] = None  # Explanation (optional)


class ProofQuestion(BaseExample):
    """Proof question"""
    model_config = ConfigDict(strict=False)
    
    proof_id: Optional[str] = None  # ID for the proof field
    proof: str  # Proof steps (required)


class ShortAnswerQuestion(BaseExample):
    """Short-answer question"""
    model_config = ConfigDict(strict=False)
    
    answer_id: Optional[str] = None  # ID for the answer field
    explanation_id: Optional[str] = None  # ID for the explanation field
    
    answer: str  # Answer text (required)
    explanation: Optional[str] = None  # Explanation (optional)


class CodeQuestion(BaseExample):
    """Programming question"""
    model_config = ConfigDict(strict=False)
    
    answer_id: Optional[str] = None  # ID for the answer field
    explanation_id: Optional[str] = None  # ID for the explanation field
    
    code_answer: str  # Code solution (required)
    explanation: Optional[str] = None  # Explanation (optional)


# An Example can be any of these question types.
Example = Union[
    MultipleChoiceQuestion,
    FillBlankQuestion,
    ProofQuestion,
    ShortAnswerQuestion,
    CodeQuestion
]


class ExerciseList(BaseModel):
    """List of exercises"""
    model_config = ConfigDict(strict=False)
    
    exercises: List[Example]  # List of exercises (required)


class Definition(BaseModel):
    """Definition"""
    model_config = ConfigDict(strict=False)
    
    definition_id: Optional[str] = None  # ID for the definition field
    definition: str  # Definition text (required)


class Theorem(BaseModel):
    """A theorem and its proof."""
    model_config = ConfigDict(strict=False)
    
    # IDs identify individual fields and remain optional for backward compatibility.
    id: Optional[str] = None  # Unique ID, for example "theorem_def456"
    theorem_id: Optional[str] = None  # ID for the theorem field
    proof_id: Optional[str] = None  # ID for the proof field
    
    theorem: str  # Theorem statement (required)
    proof: Optional[str] = None  # Proof text (optional)


class Summary(BaseModel):
    """Section summary"""
    model_config = ConfigDict(strict=False)
    
    summary_id: Optional[str] = None  # ID for the summary field
    summary: str  # Summary text (required)


class ConceptBlock(BaseModel):
    """A definition with related examples, notes, and theorems."""
    model_config = ConfigDict(strict=False)
    
    # IDs identify individual fields and remain optional for backward compatibility.
    id: Optional[str] = None  # Unique ID, for example "concept_block_ghi789"
    definition_id: Optional[str] = None  # ID for the definition field
    
    definition: str  # Definition (required)
    examples: List[Example] = []  # Related examples
    notes: List[str] = []  # Related notes and points to watch for (optional)
    theorems: List[Theorem] = []  # Related theorems


class Section(BaseModel):
    """Section structure"""
    model_config = ConfigDict(strict=False)
    
    # IDs identify individual fields and remain optional for backward compatibility.
    id: Optional[str] = None  # Unique ID, for example "section_jkl012"
    section_title_id: Optional[str] = None  # ID for the section_title field
    introduction_id: Optional[str] = None  # ID for the introduction field
    definition_id: Optional[str] = None  # ID for the definition field
    summary_id: Optional[str] = None  # ID for the summary field
    
    section_title: str
    introduction: str  # Introduction
    definition: str  # Definition (required)
    theorems: List[Theorem] = []  # List of zero or more theorems
    examples: List[Example] = []  # List of three to five examples or exercises
    summary: str  # Summary


