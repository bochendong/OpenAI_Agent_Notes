"""Notebook content structure models - 笔记本内容结构模型"""

from __future__ import annotations

from typing import Optional, List, Literal, Dict, Union
from pydantic import BaseModel, ConfigDict


class BaseExample(BaseModel):
    """题目基类，包含所有题目类型的共同字段"""
    model_config = ConfigDict(strict=False)
    
    # ID字段（用于精确定位，支持向后兼容）
    id: Optional[str] = None  # 唯一ID，如 "example_abc123"
    question_id: Optional[str] = None  # question字段的ID
    question: str  # 题目/例子内容（必需）


class MultipleChoiceQuestion(BaseExample):
    """选择题"""
    model_config = ConfigDict(strict=False)
    
    answer_id: Optional[str] = None  # answer字段的ID
    explanation_id: Optional[str] = None  # explanation字段的ID
    
    options: List[str]  # 选项列表（必需，通常4个选项）
    correct_answer: str  # 正确答案（必需，如 "A", "B", "C", "D"）
    explanation: Optional[str] = None  # 解释（可选）


class FillBlankQuestion(BaseExample):
    """填空题"""
    model_config = ConfigDict(strict=False)
    
    answer_id: Optional[str] = None  # answer字段的ID
    explanation_id: Optional[str] = None  # explanation字段的ID
    
    blanks: Dict[str, str]  # 填空题答案字典（必需）
    # 格式：{"[空1]": "答案1", "[空2]": "答案2", ...} 或 {"blank1": "答案1", "blank2": "答案2", ...}
    # 键必须与 question 中的占位符完全匹配
    explanation: Optional[str] = None  # 解释（可选）


class ProofQuestion(BaseExample):
    """证明题"""
    model_config = ConfigDict(strict=False)
    
    proof_id: Optional[str] = None  # proof字段的ID
    proof: str  # 证明步骤（必需）


class ShortAnswerQuestion(BaseExample):
    """简答题"""
    model_config = ConfigDict(strict=False)
    
    answer_id: Optional[str] = None  # answer字段的ID
    explanation_id: Optional[str] = None  # explanation字段的ID
    
    answer: str  # 答案内容（必需）
    explanation: Optional[str] = None  # 解释（可选）


class CodeQuestion(BaseExample):
    """代码题"""
    model_config = ConfigDict(strict=False)
    
    answer_id: Optional[str] = None  # answer字段的ID
    explanation_id: Optional[str] = None  # explanation字段的ID
    
    code_answer: str  # 代码答案（必需）
    explanation: Optional[str] = None  # 解释（可选）


# 类型别名：Example 可以是任意一种题目类型
Example = Union[
    MultipleChoiceQuestion,
    FillBlankQuestion,
    ProofQuestion,
    ShortAnswerQuestion,
    CodeQuestion
]


class ExerciseList(BaseModel):
    """练习题列表"""
    model_config = ConfigDict(strict=False)
    
    exercises: List[Example]  # 练习题列表（必需）


class Definition(BaseModel):
    """定义"""
    model_config = ConfigDict(strict=False)
    
    definition_id: Optional[str] = None  # definition字段的ID
    definition: str  # 定义内容（必需）


class Theorem(BaseModel):
    """定理及其证明"""
    model_config = ConfigDict(strict=False)
    
    # ID字段（用于精确定位，支持向后兼容）
    id: Optional[str] = None  # 唯一ID，如 "theorem_def456"
    theorem_id: Optional[str] = None  # theorem字段的ID
    proof_id: Optional[str] = None  # proof字段的ID
    
    theorem: str  # 定理内容（必需）
    proof: Optional[str] = None  # 证明内容（可选）


class Summary(BaseModel):
    """章节总结"""
    model_config = ConfigDict(strict=False)
    
    summary_id: Optional[str] = None  # summary字段的ID
    summary: str  # 总结内容（必需）


class ConceptBlock(BaseModel):
    """概念块：一个定义及其相关的例子、笔记、定理等"""
    model_config = ConfigDict(strict=False)
    
    # ID字段（用于精确定位，支持向后兼容）
    id: Optional[str] = None  # 唯一ID，如 "concept_block_ghi789"
    definition_id: Optional[str] = None  # definition字段的ID
    
    definition: str  # 定义（必需）
    examples: List[Example] = []  # 相关例子列表
    notes: List[str] = []  # 相关笔记/注意点（可选）
    theorems: List[Theorem] = []  # 相关定理列表


class Section(BaseModel):
    """章节结构"""
    model_config = ConfigDict(strict=False)
    
    # ID字段（用于精确定位，支持向后兼容）
    id: Optional[str] = None  # 唯一ID，如 "section_jkl012"
    section_title_id: Optional[str] = None  # section_title字段的ID
    introduction_id: Optional[str] = None  # introduction字段的ID
    definition_id: Optional[str] = None  # definition字段的ID
    summary_id: Optional[str] = None  # summary字段的ID
    
    section_title: str
    introduction: str  # 介绍
    definition: str  # 定义（必需）
    theorems: List[Theorem] = []  # 定理列表（0到多个）
    examples: List[Example] = []  # 例子/练习题列表（3-5个）
    summary: str  # 总结


