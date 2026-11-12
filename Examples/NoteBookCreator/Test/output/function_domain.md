# Domain of a Function

## Introduction

This section introduces the domain of a function, how to determine it, and common restrictions to watch for. Definitions, a worked example, and exercises show how to combine those restrictions.

## Definition

The domain of a function is the set of all its allowed inputs, often denoted by `D`. When a real-valued expression is given without an explicit domain, its natural domain consists of all real inputs for which the expression is defined.

## Theorems

### Theorem 1

To find the natural domain of a real-valued expression, take the intersection of the conditions required for each operation:

1. Every denominator must be nonzero.
2. Every even root must have a nonnegative radicand.
3. Every logarithm must have a positive argument and a positive base other than 1.
4. Every trigonometric function must be defined at its argument. For example, `tan(x)` is undefined when `x = π/2 + kπ` for an integer `k`.

**Proof**

For an input to be in the natural domain, every operation in the expression must be defined. List the operations that restrict the domain, such as division, even roots, logarithms, and trigonometric or inverse trigonometric functions. Solve each restriction for `x`. An input belongs to the domain exactly when it satisfies every restriction, so the domain is the intersection of their solution sets.

For example, consider `f(x) = sqrt(x - 1) / (x² - 4) + log₂(x - 1)`.

1. The square root requires `x - 1 ≥ 0`, so `x ≥ 1`.
2. The denominator requires `x² - 4 ≠ 0`, so `x ≠ 2` and `x ≠ -2`.
3. The logarithm requires `x - 1 > 0`, so `x > 1`.

Combining these conditions gives the domain `(1, 2) ∪ (2, ∞)`.

## Exercises

### Question 1

**Question:** Which option best describes the domain of a function?

**Options:**

- A. The set of all allowed input values
- B. The set of inputs that make the function equal to zero
- C. The set of all output values
- D. An arbitrary set of real numbers

**Correct answer:** A

**Explanation:** The domain contains exactly the allowed inputs. Option B describes the zeros of the function and option C describes its range. Option D gives no criterion for membership in the domain.

### Question 2

**Question:** Let `A = {1, 2, 3, 4}` and `B = {2, 3, 5}`. A function `f(x)` is defined only for values of `x` that belong to both sets. Its domain is [blank1].

**Answer:**

- [blank1]: `{2, 3}`

**Explanation:** The domain is `A ∩ B = {2, 3}`.

### Question 3

**Question:** Which set operation gives the inputs that belong to both `A` and `B`?

**Options:**

- A. The union of `A` and `B`
- B. The intersection of `A` and `B`
- C. The difference `A \ B`
- D. The difference `B \ A`

**Correct answer:** B

**Explanation:** An intersection contains elements common to both sets. A union includes elements from either set, and a set difference includes elements found only in its first operand.

### Question 4

**Question:** Find the domain of `f(x) = 1/√(x - 1)` and briefly explain your reasoning.

**Answer:** `x > 1`

**Explanation:** The square root requires `x - 1 ≥ 0`. Since the square root is in the denominator, it must also be nonzero. Together, the conditions give `x - 1 > 0`.

## Summary

### 1. What the domain describes

- The domain is the set of allowed inputs.
- For a formula `y = f(x)` with no stated domain, check which values of `x` produce a defined result.

### 2. How to find the domain

1. Check each operation in the expression.
   - Exclude any inputs that make a denominator zero.
   - For an even root such as `√g(x)`, require `g(x) ≥ 0`.
   - For a logarithm such as `ln g(x)`, require `g(x) > 0`.
   - For a standard exponential function `aˣ`, the base `a` is positive and different from 1.
   - For a piecewise function, apply the stated input restrictions for each piece.
2. When an expression has multiple restrictions, intersect the sets of inputs that satisfy them.

### 3. Common domains

- Linear, quadratic, and other polynomial expressions are defined on all real numbers.
- Rational expressions exclude inputs that make the denominator zero.
- Even roots require nonnegative radicands.
- Logarithms and exponential functions follow the conditions on their arguments and bases.

### 4. Common pitfalls

- Check every restriction when several apply at once.
- When an even root occurs in a denominator, its radicand must be strictly positive.

### 5. Frequently asked questions

**Why do division, even roots, and logarithms restrict the domain?**

Division by zero is undefined. Negative numbers have no real even roots. Real logarithms are defined only for positive arguments.

### 6. Study tips

- Review each operation in the expression for possible restrictions.
- Practice expressing domains using inequalities, interval notation, and sets.
