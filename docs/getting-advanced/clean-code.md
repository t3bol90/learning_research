# Clean code

Excerpted from this document: [https://segmentfault.com/a/1190000019565037](https://segmentfault.com/a/1190000019565037)

## Naming

### 1. Avoid misleading names

- For "a group of accounts", do not use **accountList**. **List** has a specific meaning to programmers. Use **accountGroup**, **bunchOfAccounts**, or even **accounts**.
- **Do not use names that differ only slightly.** ZYXControllerForEfficientHandlingOfStrings and ZYXControllerForEfficientStorageOfStrings are hard to tell apart.
- Do not use lowercase l or uppercase O as variable names. They look like the constants 1 and 0.

### 2. Make meaningful distinctions

- **Do not name things in number sequences** (a1, a2, a3). Name things by what they actually mean.
- **Product / ProductInfo / ProductData** mean the same thing. Pick one and stick with it.
- Do not write redundant names. Variable names should not contain **variable**, and table names should not contain **table**.

### 3. Use searchable names

- Single-letter names and numeric constants are hard to find in context. Name length should match scope size. **The more often a variable name appears, the easier (and longer) it should be to search.**

### 4. Avoid encodings in names

- Encoding the type and scope into the name adds decoding overhead. New people then have to learn this **encoded language** on top of the actual code logic.
- Do not use **Hungarian notation** (format: **\[Prefix\]-BaseTag-Name**, where BaseTag is an abbreviation of the data type and Name is the variable name). It is just clutter.
- You do not need an "m_" prefix to mark member variables.
- Do not encode "interface" and "implementation" into names. The leading **"I"** in **IShapeFactory** is **noise**. If you have to encode one of the two, encode the implementation. **ShapeFactoryImp** is better than encoding the interface name.

### 5. Class names and method names

- **Class names should be nouns** or noun phrases. **Method names should be verbs** or verb phrases.

### 6. One word per concept

- Pick one of **fetch, retrieve, get** and use it consistently.

### 7. Do not use puns

- The usual meaning of an **add** method is: take two values and produce a new value. **If you want to put a single value into a collection**, **insert** or **append** is a better name. Calling it **add** is a pun.

### 8. Add meaningful context

- Few names explain themselves. **You need well-named classes, functions, or namespaces around them** to give the reader context. If that is not possible, adding a prefix to the name is the last resort.

## Functions

### 1. Shorter is better

- The body of an **if / else / while statement** should be one line, and that line should be a function call.
- The indentation of a function should not be more than one or two levels deep.

### 2. Do one thing

- A function does one thing if everything it does sits at the **same level of abstraction** suggested by its name.
- To check whether a function does more than one thing, ask whether you can **extract another function** out of it.

### 3. One level of abstraction per function

### 4. switch statements

- **Bury the switch low in the abstraction layers.** Usually it can sit inside an abstract factory and be used to create polymorphic objects.

### 5. Use descriptive names

- The shorter and more focused a function is, the easier it is to give it a good name.
- Do not be afraid of long names. **A long, descriptive name is better than a short, cryptic one and better than a long descriptive comment.**
- Do not be afraid to spend time on naming.

### 6. Function arguments

- **The fewer arguments, the better.** Zero is best. Try to avoid more than three.
- The more arguments there are, the harder it is to write tests that cover all combinations.
- **Do not use flag arguments.** Passing a **bool** into a function is a bad sign. It means the function does more than one thing. Split it into two functions.
- If a function needs **two, three, or more arguments**, that often means **some of those arguments should be wrapped into a class**.
- **Encode argument order into the function name** so the reader does not have to remember it. For example, assertExpectedEqualsActual(expected, actual).

### 7. Side effects (the impact a function has on the outside world beyond its main job)

- A method that checks a password and also initialises a session should be named checkPasswordAndInitializeSession, not checkPassword. **Even if this breaks the single responsibility principle, it is better than hiding a side effect.**
- Avoid "output arguments". **If a function has to change some state, change the state of the object it belongs to.**

### 8. Separate setting (writing) from querying (reading)

- The meaning of `if(set("username", "unclebob")) { ... }` is unclear. Rewrite it as:

	```plain text
if (attributeExists("username")) {
    setAttribute("username", "unclebob");
    ...
}
	```

### 9. Use exceptions instead of returning error codes

- **Returning error codes** forces the caller to handle the error immediately, which **leads to deeply nested structures**:

	```plain text
if (deletePate(page) == E_OK) {
    if (xxx() == E_OK) {
        if (yyy() == E_OK) {
            log();
        } else {
            log();
        }
    } else {
        log();
    }
} else {
    log();
}
	```

- Using exceptions:

	```plain text
try {
    deletePage();
    xxx();
    yyy();
} catch (Exception e) {
    log(e->getMessage());
}
	```

- try/catch blocks are ugly, so **it is best to pull the bodies of the try and catch blocks out into their own functions**:

	```plain text
try {
    do();
} catch (Exception e) {
    handle();
}
	```

- A function does one thing, and error handling is one thing. **If the keyword try appears in a function, it should be the first word in the function, and there should be nothing after the catch block.**
- A class that defines error codes has a problem: **when you add a new error code, every other class that uses that error code class has to be recompiled and redeployed.** With exceptions instead of error codes, **a new exception can be derived from an existing exception class without recompiling or redeploying anything else.** This is an example of the open closed principle (open for extension, closed for modification).

### 10. Do not write duplicate code

- Duplication is the root of all evil in software. When the algorithm changes, you have to change it in many places.

### 11. Structured programming

- As long as functions stay short, the occasional **return, break, or continue** does no harm and can be more expressive than the strict single-entry single-exit rule. **goto** only makes sense in large functions, so you should avoid it.

### 12. How to write functions like this

- You do not have to write functions this way from the start. Nobody can. Write whatever comes to mind, then polish the code and shape the functions to fit these rules.

## Comments

- If the programming language is expressive enough, we do not need comments.
- A comment is always a sign of failure.
- Code evolves, but comments do not always evolve with it.
- An inaccurate comment is much worse than no comment.

### 1. Explain in code

- Just create a function that says the same thing the comment says.

	```plain text
// check to see if the employee is eligible for full benefits
if ((employee.falgs & HOURLY_FLAG) && (employee.age > 65))
	```

	should become

	```plain text
if (employee.isEligibleForFullBenefits())
	```

### 2. Good comments

- Legal information.
- Basic information, such as explaining what an **abstract method returns**.
- Explanation of intent that shows the reasoning behind a decision.
- Clarification. Translating the meaning of **obscure arguments or return values** into something readable (the better fix is to make them clear on their own, but for things like the standard library we cannot change the source):

	```plain text
if (b.compareTo(a) == 1) //b > a
	```

- Warnings. `// don't run unless you have some time to kill`
- **TODO** comments.
- Highlighting the importance of something that looks unreasonable.

### 3. Bad comments

- Talking to yourself.
- Redundant comments. **Restating the logic in a comment does not add information** and is not easier to read than the code itself. **Do not put comments on member variables that are obvious.** It is just noise.
- Misleading comments.
- Comments written to follow a rule. **Putting a comment on every function and every variable is silly.**
- Journal-style comments. With version control, you do not need to keep a list of modification times and authors at the top of the file.
- **If a function or variable can express it, do not use a comment**:

	```plain text
// does the module from the global list <mod>
// depend on the subsystem we are part of?
if (smodule.getDependSubsystems().contains(subSysMod.getSubSystem())
	```

	can become

	```plain text
ArrayList moduleDependees = smodule.getDependSubsystems();
String ourSubSystem = subSysMod.getSubSystem();
if (moduleDependees.contains(ourSubSystem))
	```

- Position markers. **If you use too many, we tune them out**: `///////////////////// Actions //////////////////////////`
- Closing brace comments.

	```plain text
try {
    while () {
        if () {
            ...
        } // if
        ...
    } // while
    ...
} // try
	```

	If you feel the need to mark a closing brace, what you actually need is a shorter function.
- Attributions. `/* add by rick */` Source control already remembers you, and **attribution comments do not keep up with code changes.**
- Commented-out code. Other people who see it will be afraid to delete it.
- Too much information. Do not put interesting historical anecdotes or unrelated details in a comment.
- Comments that do not actually explain anything. The point of a comment is to explain code that cannot explain itself. It is a shame if the comment itself needs explaining.
- Header comments on short functions. **A good name on a short function is better than a header comment.**
- javadoc / phpdoc comments on non-public APIs.

## Code formatting

### 1. Vertical formatting

- Short files are easier to understand than long ones. **A file averaging 200 lines, never more than 500, can build excellent systems.**
- Separation: package declaration, import declaration, and each function should be separated by blank lines. **A blank line marks the start of a new, distinct concept.**
- Closeness: closely related code should sit close together. For example, **do not put blank lines between fields inside a class.**
- **Variable declarations should sit as close to where they are used as possible**: a loop control variable should always be declared inside the loop statement.
- **Member variables should be declared at the top of the class**, not scattered around.
- **If one function calls another, they should sit near each other.** We want low-level details to appear last so the reader does not get lost in them, so **the caller should sit above the callee where possible.**
- A few functions that do the same basic job should sit together.

### 2. Horizontal formatting

- A line of code does not have to stick rigidly to an 80-character limit. The occasional 100 characters, but not over 120, is fine.
- Separation and closeness: spaces emphasise the split between left and right. **Put spaces on both sides of an assignment operator. Do not put a space between a function name and the left parenthesis. When a multiplication operator combines with a plus or minus, do not add spaces around it (a\*b - c).**
- You do not have to align horizontally. For example, when you declare a stack of member variables, you do not need to align every word in each line.
- Even a short if, while, or function should not break the indentation rule. Do not write things like: `if (xx == yy) z = 1;`

## Objects and data structures

Objects expose behaviour (an interface) and hide data (private variables).
Data structures have no real behaviour (no interface) and expose data. Examples include DTOs (Data Transfer Objects) and entities.

### 1. The asymmetry between objects and data structures (see code listing 6-5 in the book)

- Using **data structures makes it easy to add new functions** without changing the existing data structures. Using **objects makes it easy to add new classes** without changing existing functions.
- Using **data structures makes it hard to add new data structures**, because you have to change every function. Using **objects makes it hard to add new functions**, because you have to change every class.
- "Everything is an object" is a myth. Sometimes we do procedural work on simple data structures.

### 2. The Law of Demeter (the principle of least knowledge)

- **A module should not know about the internals of the objects it uses.**
- A method f of class C should only call methods on:
	- C
	- objects created inside f
	- objects passed in as arguments to f
	- objects held by C
- A method should not call methods on **objects returned by another function**. The line below breaks the Law of Demeter: `final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();`
- A simple example: a person can tell a dog to walk, but should not directly tell the dog's legs to walk. The dog should tell its own legs how to walk.

## Exception handling

Exception handling matters. But if exception handling is scattered across the code so that the logic becomes unclear, it is wrong.

### 1. Use exceptions instead of returning error codes

- With error codes, the caller has to **handle the error as soon as the function returns**, and we tend to forget.
- Error codes usually lead to **nested if/else**.

### 2. Write the try-catch first

- When you write code that may throw, write the **try-catch** first and then put the logic inside.

### 3. Use unchecked exceptions (Java only)

### 4. Inside catch, log as much information as you can. Record the operation that failed and the type of failure.

### 5. Define different exception classes based on what the caller needs

- If you have one try block that catches several different exceptions but the handling (logging, etc.) is the same, you can **wrap the exception handling in a function**. For each different exception, just throw it as the same exception without doing anything else, and handle it uniformly in the outer catch (logging, etc.). **If you only want to catch some of the exceptions and let the others pass through, use different functions to wrap the handling.**

### 6. Special case pattern: create a class to handle the special case.

```plain text
try {
    MealExpendses expenses = expenseRepotDAO.getMeals(employee.getID());
    m_total += expenses.getTotal();// if meals were consumed, add to the total
} catch (MealExpensesNotFound e) {
    m_total += getMealPeDiem();// if no meals were consumed, add the per diem to the total
}
```

The exception interrupts the business logic. You can change getMeals() so it does not throw, and instead returns a special MealExpense object (PerdiemMealExpense) when no meals were consumed, with getTotal() overridden.

```plain text
MealExpendses expenses = expenseRepotDAO.getMeals(employee.getID());
m_total += expenses.getTotal();

publc class PerDiemMealExpenses implements MealExpenses {
    public int getTotal() {
        //return xxx; //return the per diem
    }
}

```

### 7. Do not return null

- If you return null, a single missing null check anywhere will crash the application.
- When you feel like returning null, **try throwing an exception or returning a special case object instead.**

### 8. Do not pass null

- Passing null into a method is a bad practice and should be avoided.
- You can filter null arguments inside the method with if or assert, but you will still get runtime errors. There is no good way to deal with a caller who accidentally passes null. The right answer is to **forbid passing null.**

## Boundaries

Cleanly fold third-party code into your own code.

### 1. Avoid letting public APIs return boundary interfaces, and avoid passing boundary interfaces in as arguments. Keep boundaries inside close-relative classes.

### 2. Do not experiment with new things in production code. Write tests to learn third-party code.

### 3. Avoid letting our code know too much about specific details inside third-party code.

## Unit testing

### 1. The three laws of TDD (test-driven development)

- *First Law: You may not write production code until you have written a failing unit test.*
- *Second Law: You may not write more of a unit test than is sufficient to fail, and not compiling is failing.*
- *Third Law: You may not write more production code than is sufficient to pass the currently failing test.*

### 2. Keep tests clean

- **Dirty tests are the same as no tests.** The dirtier the test code, the harder the production code is to change.
- Test code matters as much as production code.
- The most important quality of clean test code is **cleanness**. **Test code should not have a lot of repeated calls.**

### 3. One assert per test

- Each test function should have **one and only one assert statement.**
- Each test function should **test one concept.**

### 4. Clean tests follow the FIRST rules

- fast: tests should **run quickly**, because we run them often.
- independent: tests should be **independent of each other**. A test should not depend on the result of a previous test, and tests should be runnable in any order.
- repeatable: tests should pass in any environment.
- self-validating: tests should output a **bool**. You should not need to read logs to confirm a test result, and you should not need to manually compare two text files.
- timely: write tests on time. **Unit tests should be written before the production code**, otherwise the production code becomes hard to test.

## Classes

### 1. Class layout (in order):

- public static constants
- private static variables
- private instance variables
- public functions
- private utility functions

### 2. Classes should be short

- For functions, we measure size by **line count**. For classes, we measure by **responsibility**.
- **The class name should describe its responsibility.** Naming is the first way to judge class length: if you cannot give a class an accurate name, it is too long. If a class name contains vague words like **Processor, Manager, Super**, that suggests **inappropriate clumping of responsibilities**.
- Single responsibility principle: a class or module should have one responsibility, that is, only one reason to change (*A class should have only one reason to change.*).
- A system should be made of **many short classes** rather than **a few large ones**.
- A class should have only a small number of instance variables. If **every instance variable in a class is used by every method**, the class has **maximum cohesion**. Maximum cohesion is not realistic, but high cohesion is the target. **The higher the cohesion, the more the methods and variables in the class depend on and combine with each other to form a single logical whole.**
- **Keeping cohesion gives you many short classes.** If you want to break out a small piece of a large function into its own function, and that new function uses 4 of the variables from the large function, you do not have to **pass those 4 variables in as arguments**. You can just **promote those 4 variables to instance variables of the class containing the large function**. But that hurts class cohesion because there are more instance variables. The better answer is **to pull those 4 variables out into their own class**. Splitting a large function into small ones is often a sign that it is time to split a class into smaller classes.

### 3. Organise for change (see code listings 10-9 and 10-10 in the book)

- Classes should be open for extension and closed for modification (the open closed principle).
- In an ideal system, we add new features by extending the system, not by modifying existing code.

## System

### 1. Separate construction of the system from its use

- **Move all construction into main**, or into the module called main. When you reach the rest of the system, **assume that all objects have been constructed correctly.**
- Sometimes the application also needs to decide when to create objects. We can use the **abstract factory pattern** to let the application **control when objects get created**, while keeping **the construction logic inside the factory implementation class**, separate from the use.
- **Dependency injection (DI) and inversion of control (IoC)** are powerful ways to separate construction from use.

## Emergent design

Four rules to help you build a good design.

### 1. Run all the tests

- Tightly coupled code is hard to test. The more tests you write, the more you end up following rules like dependency injection, which reduces coupling in the code.
- Tests remove the fear that cleaning up code will break it.

### 2. Remove duplication

- Pull common parts of two methods into a new method, and pull that new method into another class to raise its visibility.
- The **template method pattern** is a general technique for removing duplication.

	```plain text
// original logic
public class VacationPolicy() {
    public void accrueUSDivisionVacation() {
        //do x;
        //do US y;
        //do z;
    }
    public void accrueEUDivisionVacation() {
        //do x;
        //do EU y;
        //do z;
    }
}

// after refactoring with template method
abstract public class VacationPolicy {
    public void accrueVacation() {
        x();
        y();
        z();
    }
    private void x() {
        //do x;
    }
    abstract protected void y() {

    }
    private void z() {
        //do z;
    }
}
public class USVacationPolicy extends VacationPolicy {
    protected void y() {
        //do US y;
    }
}
public class EUVacationPolicy extends VacationPolicy {
    protected void y() {
        //do EU y;
    }
}

	```

### 3. Express intent

- The clearer the author writes the code, the faster others understand it.
- Too often we get deep into the problem we are solving, write code that works, and then jump to the next problem without spending the time to shape the code so the next person can read it. Show some respect for our craft. Spend a little time on every function and class.

### 4. Keep the number of classes and methods small

- To keep classes and functions short, we may end up creating too many tiny classes and methods.
- Too many classes and methods is sometimes the result of meaningless dogma.

### 5. The four rules above are listed in decreasing priority. The important ones are tests, removing duplication, and expressing intent.

## Concurrent programming

### 1. Principles and tips for guarding against concurrency problems

- Follow the single responsibility principle. Separate concurrent code from non-concurrent code.
- Limit the number of critical sections, and limit access to shared data.
- Avoid sharing data. Use copies of objects.
- Keep threads as independent as possible. Do not share data with other threads.
