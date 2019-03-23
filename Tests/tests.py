from app import *

# Testing the 'checkAllergens' function of the app.py

def test_checkAllergens_Function():
    testVal1 = {"recipe_title": "Test", "containsAllergens": True, "recipeAllergens": "Test"}
    testVal2 = {"recipe_title": "Test", "containsAllergens": False, "recipeAllergens": "Test"}
    testVal3 = {"recipe_title": "Test", "recipe_description": "A test recipe"}

    # test with a dictionary which contains a 'containsAllergens' entry, it should return True
    assert containsAllergens(testVal1) == True

    # test with a dictionary which contains a 'containsAllergens' entry but with a different value, it should still return True
    assert containsAllergens(testVal2) == True

    # test with a dictionary which contains no 'containsAllergens' entry at all, it should return False
    assert containsAllergens(testVal3) == False

    print("Result of Testing 'containsAllergens' function: All Tests Passed")


def test_listifyDict_Function():
    test1Input = "Hello\r\nWorld\r\nand\r\nEveryone\r\nElse"
    test1ExpectedResult = [{"list_item": "Hello"}, {"list_item": "World"},{"list_item": "and"}, {"list_item": "Everyone"}, {"list_item": "Else"}]

    # test with an input which contains a various number of carriage returns and new line escape characters (\r\n), the expected result is a list of
    # multiple dict key-value pairs
    assert test1ExpectedResult == listifyDict(test1Input)

    test2Input = "Hello World"
    test2ExpectedResult = [{"list_item": "Hello World"}]
    
    # test with an input which contains no carriage returns and new line escape character (\r\n) entries, the expected result is a list which contains a 
    # single key-value dict; the value of the dict should be the exact same as the input
    assert test2ExpectedResult == listifyDict(test2Input)

    print("Result of Testing 'listifyDict' function: All Tests Passed")

if __name__ == "__main__":
    test_checkAllergens_Function()
    test_listifyDict_Function()