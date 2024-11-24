from pyswip import Prolog
import re

prolog = Prolog()
# Load the family.pl file
prolog.consult("family_rules.pl")

def add_fact(statement):
    statement = statement.lower()

    def check_conflict(name, gender):
        """Check for gender conflicts before adding facts."""
        conflicting_gender = "male" if gender == "female" else "female"
        
        # Check if the conflicting gender fact exists in the knowledge base
        try:
            conflict_check = list(prolog.query(f"{conflicting_gender}({name})"))
            if conflict_check:
                return f"Error: {name.capitalize()} cannot be both male and female."
        except Exception as e:
            # If the query throws an exception (fact doesn't exist), continue as there is no conflict
            pass

        return None

    if "is the father of" in statement:
        name1, name2 = statement.split(" is the father of ")
        conflict_message = check_conflict(name1, "male")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"parent({name1}, {name2})")
        add_prolog_fact(f"male({name1})")

    elif "is the mother of" in statement:
        name1, name2 = statement.split(" is the mother of ")
        conflict_message = check_conflict(name1, "female")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"parent({name1}, {name2})")
        add_prolog_fact(f"female({name1})")

    elif "is a brother of" in statement:
        name1, name2 = statement.split(" is a brother of ")
        conflict_message = check_conflict(name1, "male")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"sibling({name1}, {name2})")
        add_prolog_fact(f"male({name1})")

    elif "is a sister of" in statement:
        name1, name2 = statement.split(" is a sister of ")
        conflict_message = check_conflict(name1, "female")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"sibling({name1}, {name2})")
        add_prolog_fact(f"female({name1})")

    elif "is an uncle of" in statement:
        name1, name2 = statement.split(" is an uncle of ")
        conflict_message = check_conflict(name1, "male")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"uncle({name1}, {name2})")

    elif "is an aunt of" in statement:
        name1, name2 = statement.split(" is an aunt of ")
        conflict_message = check_conflict(name1, "female")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"aunt({name1}, {name2})")

    elif "is the grandparent of" in statement:
        name1, name2 = statement.split(" is the grandparent of ")
        add_prolog_fact(f"grandparent({name1}, {name2})")

    elif "is a grandmother of" in statement:
        name1, name2 = statement.split(" is a grandmother of ")
        conflict_message = check_conflict(name1, "female")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"grandmother({name1}, {name2})")

    elif "is a grandfather of" in statement:
        name1, name2 = statement.split(" is a grandfather of ")
        conflict_message = check_conflict(name1, "male")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"grandfather({name1}, {name2})")

    elif "is a child of" in statement:
        name1, name2 = statement.split(" is a child of ")
        add_prolog_fact(f"child({name1}, {name2})")

    elif "are and children of" in statement:
        names = statement.replace(" are and children of ", "").split(" and ")
        for name in names:
            add_prolog_fact(f"child({name}, {names[-1]})")

    elif "is a daughter of" in statement:
        name1, name2 = statement.split(" is a daughter of ")
        conflict_message = check_conflict(name1, "female")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"daughter({name1}, {name2})")

    elif "is a son of" in statement:
        name1, name2 = statement.split(" is a son of ")
        conflict_message = check_conflict(name1, "male")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"son({name1}, {name2})")

    else:
        return "I don't understand this statement."
    
    return "OK! I learned something."


def add_prolog_fact(fact):
    try:
        prolog.assertz(fact)  # Add the fact to the Prolog knowledge base
        return "Fact added successfully."
    except Exception as e:
        return f"Error adding fact: {str(e)}"


def ask_question(question):
    question = question.lower()

    patterns = [
    (r"are (\w+) and (\w+) siblings\?", lambda m: f"sibling({m[0]}, {m[1]})."),
    (r"is (\w+) a brother of (\w+)\?", lambda m: f"sibling({m[0]}, {m[1]}), male({m[0]})."),
    (r"is (\w+) a sister of (\w+)\?", lambda m: f"sibling({m[0]}, {m[1]}), female({m[0]})."),

    (r"is (\w+) the father of (\w+)\?", lambda m: f"parent({m[0]}, {m[1]}), male({m[0]})."),
    (r"is (\w+) the mother of (\w+)\?", lambda m: f"parent({m[0]}, {m[1]}), female({m[0]})."),
    (r"are (\w+) and (\w+) the parents of (\w+)\?", lambda m: f"parent({m[0]}, {m[2]}), parent({m[1]}, {m[2]})."),
    
    (r"is (\w+) a grandmother of (\w+)\?", lambda m: f"grandmother({m[0]}, {m[1]})."),
    (r"is (\w+) a grandfather of (\w+)\?", lambda m: f"grandfather({m[0]}, {m[1]})."),

    (r"is (\w+) a child of (\w+)\?", lambda m: f"child({m[0]}, {m[1]})."),
    (r"are (\w+) and (\w+) children of (\w+)\?", lambda m: f"child({m[0]}, {m[2]}), child({m[1]}, {m[2]})."),
    (r"is (\w+) a daughter of (\w+)\?", lambda m: f"daughter({m[0]}, {m[1]})."),
    (r"is (\w+) a son of (\w+)\?", lambda m: f"son({m[0]}, {m[1]})."),

    (r"is (\w+) an uncle of (\w+)\?", lambda m: f"uncle({m[0]}, {m[1]})."),
    (r"is (\w+) an aunt of (\w+)\?", lambda m: f"aunt({m[0]}, {m[1]})."),
    ]

    for pattern, handler in patterns:
        match = re.match(pattern, question)
        if match:
            return query_prolog(handler(match.groups()))  # Use groups directly
    return "I don't understand this question."

def query_prolog(query):
    try:
        results = list(prolog.query(query))
        return "Yes!" if results else "No."
    except Exception as e:
        return f"Error in query: {str(e)}"

if __name__ == "__main__":
    print("Family Relations Chat Bot (type 'exit' to quit)")
    print("You can make statements like:")
    print("- John is the father of Mary")
    print("- Sarah is the mother of John")
    print("Or ask questions like:")
    print("- Is John the father of Mary?")
    print("- Are John and Mary siblings?")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if re.search(r"\?$", user_input):  
            response = ask_question(user_input)
        else:  
            response = add_fact(user_input)
        
        print("Bot:", response)
