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
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        
        if list(prolog.query(f"older( {name2}, {name1})")): # doesn't allow descendants to be their parents' parents or anything 
            return "You can't do that. Time doesn't work that way!" 

        if list(prolog.query(f"father( X, {name2})")): # only allows for 1 father 
            return "%s already has a father." % (name2)
        

        if conflict_message:
            return conflict_message
        add_prolog_fact(f"parent({name1}, {name2})")
        add_prolog_fact(f"male({name1})")
        

    elif "is the mother of" in statement:
        name1, name2 = statement.split(" is the mother of ")
        conflict_message = check_conflict(name1, "female")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        
        if list(prolog.query(f"older( {name2}, {name1})")): # doesn't allow descendants to be their parents' parents or anything 
            return "You can't do that. Time doesn't work that way!" 
        
        if list(prolog.query(f"mother( X, {name2})")): # only allows for 1 mother 
            return "%s already has a mother." % (name2)

        if conflict_message:
            return conflict_message
        add_prolog_fact(f"parent({name1}, {name2})")
        add_prolog_fact(f"female({name1})")

    elif "is a brother of" in statement:
        name1, name2 = statement.split(" is a brother of ")
        conflict_message = check_conflict(name1, "male")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        if conflict_message:
            return conflict_message
        
        add_prolog_fact(f"sibling({name1}, {name2})")
        add_prolog_fact(f"male({name1})")
        return "I learned something! kinda..."


    elif "is a sister of" in statement:
        name1, name2 = statement.split(" is a sister of ")
        conflict_message = check_conflict(name1, "female")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"sibling({name1}, {name2})")
        add_prolog_fact(f"female({name1})")
        return "I learned something! kinda..."
    
    elif "and" in statement and "are siblings" in statement:
        names = statement.replace(" are siblings", "").split(" and ")
        if len(names) == 2:
            name1, name2 = names[0].strip(), names[1].strip()
            add_prolog_fact(f"sibling({name1}, {name2})")
            add_prolog_fact(f"sibling({name2}, {name1})")
            return "I learned something! kinda..."
        else:
            return "Error: Invalid sibling statement format."
        

    elif "and" in statement and "are the parents of" in statement:
        names, child = statement.split(" are the parents of ")
        parent1, parent2 = names.split(" and ")
        parent1, parent2, child = parent1.strip(), parent2.strip(), child.strip()

        if parent1 == parent2 or parent1 == child or parent2 == child:
            return "A person cannot have such a relationship with themselves."
        
        if list(prolog.query(f"older( {name2}, {name1})")): # doesn't allow descendants to be their parents' parents or anything 
            return "You can't do that. Time doesn't work that way!" 
        
        add_prolog_fact(f"parent({parent1}, {child})")
        add_prolog_fact(f"parent({parent2}, {child})")
    
    elif "and" in statement and "are children of" in statement:
        names, parent = statement.split(" are children of ")
        # Split children by commas and "and", and clean up whitespace
        children = [name.strip() for name in names.replace(" and ", ",").split(",")]

        # Validate for duplicates or self-references
        if len(children) != len(set(children)):
            return "Error: Duplicate names found in the list of children."
        if parent.strip() in children:
            return "Error: A person cannot be their own parent."
        
        # Add facts for each child
        for child in children:
            add_prolog_fact(f"child({child}, {parent.strip()})")

    elif "is an uncle of" in statement:
        name1, name2 = statement.split(" is an uncle of ")
        conflict_message = check_conflict(name1, "male")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        
        if list(prolog.query(f"older( {name2}, {name1})")): # doesn't allow descendants to be their parents' parents or anything 
            return "You can't do that. Time doesn't work that way!" 
        
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"uncle({name1}, {name2})")
        add_prolog_fact(f"male({name1})")

    elif "is an aunt of" in statement:
        name1, name2 = statement.split(" is an aunt of ")
        conflict_message = check_conflict(name1, "female")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        
        if list(prolog.query(f"older( {name2}, {name1})")): # doesn't allow descendants to be their parents' parents or anything 
            return "You can't do that. Time doesn't work that way!" 
        
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"aunt({name1}, {name2})")
        add_prolog_fact(f"female({name1})")

    elif "is the grandparent of" in statement:
        name1, name2 = statement.split(" is the grandparent of ")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        if list(prolog.query(f"older( {name2}, {name1})")): # doesn't allow descendants to be their parents' parents or anything 
            return "You can't do that. Time doesn't work that way!" 
        add_prolog_fact(f"grandparent({name1}, {name2})")

    elif "is a grandmother of" in statement:
        name1, name2 = statement.split(" is a grandmother of ")
        conflict_message = check_conflict(name1, "female")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        if list(prolog.query(f"older( {name2}, {name1})")): # doesn't allow descendants to be their parents' parents or anything 
            return "You can't do that. Time doesn't work that way!" 
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"grandmother({name1}, {name2})")
        add_prolog_fact(f"female({name1})")

    elif "is a grandfather of" in statement:
        name1, name2 = statement.split(" is a grandfather of ")
        conflict_message = check_conflict(name1, "male")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        if list(prolog.query(f"older( {name2}, {name1})")): # doesn't allow descendants to be their parents' parents or anything 
            return "You can't do that. Time doesn't work that way!" 
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"grandfather({name1}, {name2})")
        add_prolog_fact(f"male({name1})")

    elif "is a child of" in statement:
        name1, name2 = statement.split(" is a child of ")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        
        if list(prolog.query(f"younger( {name2}, {name1})")): # doesn't allow older people to be their own children
            return "You can't do that, Time doesn't work that way!" 
        
        add_prolog_fact(f"child({name1}, {name2})")
        add_prolog_fact(f"parent({name2}, {name1})")

    elif "are and children of" in statement:
        names = statement.replace(" are and children of ", "").split(" and ")
        #uhhh if theres duplicates of a name, error
        for name in names:
            add_prolog_fact(f"child({name}, {names[-1]})")

    elif "is a daughter of" in statement:
        name1, name2 = statement.split(" is a daughter of ")
        conflict_message = check_conflict(name1, "female")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        
        if list(prolog.query(f"younger( {name2}, {name1})")): # doesn't allow older people to be their own children
            return "You can't do that, Time doesn't work that way!" 
        
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"daughter({name1}, {name2})")
        add_prolog_fact(f"female({name1})")

    elif "is a son of" in statement:
        name1, name2 = statement.split(" is a son of ")
        conflict_message = check_conflict(name1, "male")
        if name1 == name2:
            return "%s cannot be two different people." % (name1.capitalize())
        
        if list(prolog.query(f"younger( {name2}, {name1})")): # doesn't allow older people to be their own children
            return "You can't do that, Time doesn't work that way!" 

        if conflict_message:
            return conflict_message
        add_prolog_fact(f"son({name1}, {name2})")
        add_prolog_fact(f"male({name1})")

    elif "is a male" in statement:
        name = statement.replace(" is a male", "")
        conflict_message = check_conflict(name, "male")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"male({name})")

    elif "is a female" in statement:
        name = statement.replace(" is a female", "")
        conflict_message = check_conflict(name, "female")
        if conflict_message:
            return conflict_message
        add_prolog_fact(f"female({name})")

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

        (r"is (\w+) a grandparent of (\w+)\?", lambda m: f"grandparent({m[0]}, {m[1]})."),
        (r"is (\w+) a grandmother of (\w+)\?", lambda m: f"grandmother({m[0]}, {m[1]})."),
        (r"is (\w+) a grandfather of (\w+)\?", lambda m: f"grandfather({m[0]}, {m[1]})."),

        (r"is (\w+) a child of (\w+)\?", lambda m: f"child({m[0]}, {m[1]})."),
        (r"are (\w+) and (\w+) children of (\w+)\?", lambda m: f"child({m[0]}, {m[2]}), child({m[1]}, {m[2]})."),
        (r"is (\w+) a daughter of (\w+)\?", lambda m: f"daughter({m[0]}, {m[1]})."),
        (r"is (\w+) a son of (\w+)\?", lambda m: f"son({m[0]}, {m[1]})."),

        (r"is (\w+) an uncle of (\w+)\?", lambda m: f"uncle({m[0]}, {m[1]})."),
        (r"is (\w+) an aunt of (\w+)\?", lambda m: f"aunt({m[0]}, {m[1]})."),
        (r"is (\w+) a male\?", lambda m: f"male({m[0]})."),
        (r"is (\w+) a female\?", lambda m: f"female({m[0]})."),

        (r"who are the siblings of (\w+)\?", lambda m: f"sibling({m[0]}, X)."),
        (r"who are the sisters of (\w+)\?", lambda m: f"sibling({m[0]}, X), female(X)."),
        (r"who are the brothers of (\w+)\?", lambda m: f"sibling({m[0]}, X), male(X)."),
        (r"who is the mother of (\w+)\?", lambda m: f"parent(X, {m[0]}), female(X)."),
        (r"who is the father of (\w+)\?", lambda m: f"parent(X, {m[0]}), male(X)."),
        (r"who are the parents of (\w+)\?", lambda m: f"parent(X, {m[0]})."),
        (r"who are the daughters of (\w+)\?", lambda m: f"daughter(X, {m[0]})."),
        (r"who are the sons of (\w+)\?", lambda m: f"son(X, {m[0]})."),
        (r"who are the children of (\w+)\?", lambda m: f"child(X, {m[0]})."),


        (r"are (\w+) and (\w+) relatives\?", lambda m: f"related({m[0]}, {m[1]})."),
    ]

    for pattern, handler in patterns:
        match = re.match(pattern, question)
        if match:
            return query_prolog(handler(match.groups()))  # Use groups directly
    return "I don't understand this question."


def query_prolog(query):
    try:
        results = list(prolog.query(query))
        # print(results) #for debugging
        if not results:
            return "No."
        
        # Check if query contains variables (e.g., "who" questions)
        if any("X" in result for result in results):
            # Collect all unique names found in the results for variable X
            names = {result["X"] for result in results if "X" in result}
            if names:
                return f"The answer is: {', '.join(names)}."
            return "No relevant names found."
        
        return "Yes!"  # For boolean queries without variables
    except Exception as e:
        return f"Error in query: {str(e)}"

def display_facts():
    display_gender("male")
    display_gender("female")
    display_one("parent")
    display_one("sibling")
    display_one("grandfather")
    display_one("grandmother")
    display_one("uncle")
    display_one("aunt")
    display_one("child")
    display_one("daughter")
    display_one("son")
    display_one("grandparent")

def display_gender(genzzzz):
    res = list(prolog.query(f"{genzzzz}(X)"))
    for oof in res:
        print(f"{genzzzz}({oof['X']})")

def display_one(uwah):
    res = list(prolog.query(f"{uwah}(X, Y)"))
    for oof in res:
        print(f"{uwah}({oof['X']}, {oof['Y']})")


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
        #display_facts() 
