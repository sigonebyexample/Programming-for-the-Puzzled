"""
Card Mind Reading Trick
Implementation of a mathematical card trick where 5 cards are chosen,
one is hidden, and the remaining 4 are arranged in a specific order
to encode the hidden card.
"""

# Deck of 52 cards as strings: rank_suit
deck = ['A_C', 'A_D', 'A_H', 'A_S', '2_C', '2_D', '2_H', '2_S', '3_C', '3_D', '3_H', '3_S',
        '4_C', '4_D', '4_H', '4_S', '5_C', '5_D', '5_H', '5_S', '6_C', '6_D', '6_H', '6_S',
        '7_C', '7_D', '7_H', '7_S', '8_C', '8_D', '8_H', '8_S', '9_C', '9_D', '9_H', '9_S',
        '10_C', '10_D', '10_H', '10_S', 'J_C', 'J_D', 'J_H', 'J_S',
        'Q_C', 'Q_D', 'Q_H', 'Q_S', 'K_C', 'K_D', 'K_H', 'K_S']

class Card:
    """Represents a playing card with its properties."""
    
    def __init__(self, card_string):
        self.card_string = card_string
        self.index = deck.index(card_string)
        self.suit = self.index % 4
        self.number = self.index // 4
        self.rank = card_string.split('_')[0]
        self.suit_name = card_string.split('_')[1]
    
    def __str__(self):
        return self.card_string
    
    def __repr__(self):
        return f"Card('{self.card_string}')"

class CardTrick:
    """Implements the card mind reading trick."""
    
    def __init__(self):
        self.deck = deck
        self.suit_names = {'C': 'Clubs', 'D': 'Diamonds', 'H': 'Hearts', 'S': 'Spades'}
        self.rank_names = {'A': 'Ace', 'J': 'Jack', 'Q': 'Queen', 'K': 'King'}
    
    def validate_card_input(self, card_string):
        """Validate that the card exists in the deck."""
        if card_string not in self.deck:
            raise ValueError(f"Card '{card_string}' is not valid!")
        return True
    
    def get_valid_card_input(self, prompt):
        """Get valid card input from user with error handling."""
        while True:
            try:
                card_input = input(prompt).strip()
                self.validate_card_input(card_input)
                return card_input
            except ValueError as e:
                print(f"Error: {e} Please try again.")
    
    def find_matching_suit_cards(self, cards):
        """Find cards that share the same suit (at least two cards must share a suit)."""
        suit_groups = {}
        for i, card in enumerate(cards):
            if card.suit not in suit_groups:
                suit_groups[card.suit] = []
            suit_groups[card.suit].append((i, card))
        
        # Find suits with at least 2 cards
        valid_suits = {suit: cards_list for suit, cards_list in suit_groups.items() 
                      if len(cards_list) >= 2}
        
        if not valid_suits:
            raise ValueError("No matching suits found! This should not happen with 5 cards.")
        
        return valid_suits
    
    def calculate_best_encoding_pair(self, valid_suits):
        """Calculate the best pair of cards to use for encoding."""
        best_encode_value = 0
        best_pair = None
        best_hidden_index = None
        best_first_index = None
        
        for suit, cards_list in valid_suits.items():
            # Check all pairs in this suit group
            for i in range(len(cards_list)):
                for j in range(i + 1, len(cards_list)):
                    idx1, card1 = cards_list[i]
                    idx2, card2 = cards_list[j]
                    
                    # Calculate both possible encodings
                    encode1 = (card1.number - card2.number) % 13
                    encode2 = (card2.number - card1.number) % 13
                    
                    # Check if either encoding is valid (1-6)
                    if 1 <= encode1 <= 6:
                        if encode1 > best_encode_value:
                            best_encode_value = encode1
                            best_pair = (card1, card2)
                            best_hidden_index = idx1
                            best_first_index = idx2
                    
                    if 1 <= encode2 <= 6:
                        if encode2 > best_encode_value:
                            best_encode_value = encode2
                            best_pair = (card2, card1)
                            best_hidden_index = idx2
                            best_first_index = idx1
        
        if best_pair is None:
            # Fallback: use the first valid pair found
            suit = next(iter(valid_suits))
            cards_list = valid_suits[suit]
            card1_idx, card1 = cards_list[0]
            card2_idx, card2 = cards_list[1]
            encode_value = (card1.number - card2.number) % 13
            if encode_value == 0:
                encode_value = 6  # Default to max value if same rank
            
            return encode_value, card1_idx, card2_idx, card1, card2
        
        return best_encode_value, best_hidden_index, best_first_index, best_pair[0], best_pair[1]
    
    def sort_three_cards(self, cards_indices):
        """Sort three card indices in ascending order."""
        for i in range(len(cards_indices) - 1):
            min_idx = i
            for j in range(i + 1, len(cards_indices)):
                if cards_indices[j] < cards_indices[min_idx]:
                    min_idx = j
            cards_indices[i], cards_indices[min_idx] = cards_indices[min_idx], cards_indices[i]
        return cards_indices
    
    def arrange_remaining_cards(self, encode_value, remaining_indices):
        """Arrange the three remaining cards based on the encode value."""
        if encode_value == 1:
            return [remaining_indices[0], remaining_indices[1], remaining_indices[2]]
        elif encode_value == 2:
            return [remaining_indices[0], remaining_indices[2], remaining_indices[1]]
        elif encode_value == 3:
            return [remaining_indices[1], remaining_indices[0], remaining_indices[2]]
        elif encode_value == 4:
            return [remaining_indices[1], remaining_indices[2], remaining_indices[0]]
        elif encode_value == 5:
            return [remaining_indices[2], remaining_indices[0], remaining_indices[1]]
        else:  # encode_value == 6
            return [remaining_indices[2], remaining_indices[1], remaining_indices[0]]
    
    def assistant_phase(self):
        """Assistant's phase: hide one card and arrange the others."""
        print("=== ASSISTANT PHASE ===")
        print("Card format examples: A_C, 10_D, Q_H")
        print("Full deck order:", self.deck[:8], "...\n")
        
        # Get 5 cards from user
        cards = []
        for i in range(5):
            prompt = f"Enter card {i+1}: "
            card_input = self.get_valid_card_input(prompt)
            cards.append(Card(card_input))
        
        print(f"\nSelected cards: {[str(card) for card in cards]}")
        
        # Find cards with matching suits
        valid_suits = self.find_matching_suit_cards(cards)
        
        # Calculate best encoding pair
        encode_value, hidden_idx, first_idx, hidden_card, first_card = \
            self.calculate_best_encoding_pair(valid_suits)
        
        print(f"Hidden card: {hidden_card}")
        print(f"Encoding value: {encode_value}")
        
        # Prepare remaining three cards
        remaining_indices = []
        for i in range(5):
            if i != hidden_idx and i != first_idx:
                remaining_indices.append(cards[i].index)
        
        # Sort and arrange remaining cards
        sorted_indices = self.sort_three_cards(remaining_indices.copy())
        final_arrangement = self.arrange_remaining_cards(encode_value, sorted_indices)
        
        # Display the arrangement
        print(f"\nFirst card: {first_card}")
        print(f"Second card: {deck[final_arrangement[0]]}")
        print(f"Third card: {deck[final_arrangement[1]]}")
        print(f"Fourth card: {deck[final_arrangement[2]]}")
        
        return {
            'hidden_card': hidden_card,
            'first_card': first_card,
            'arrangement': [deck[final_arrangement[0]], 
                          deck[final_arrangement[1]], 
                          deck[final_arrangement[2]]],
            'encode_value': encode_value
        }
    
    def magician_phase(self):
        """Magician's phase: deduce the hidden card from the arrangement."""
        print("\n=== MAGICIAN PHASE ===")
        print("Enter the 4 cards in the order they were presented:")
        
        cards = []
        for i in range(4):
            prompt = f"Card {i+1}: "
            card_input = self.get_valid_card_input(prompt)
            cards.append(Card(card_input))
        
        # First card determines suit of hidden card
        first_card = cards[0]
        hidden_suit = first_card.suit
        hidden_number_base = first_card.number
        
        # Decode the arrangement of the last 3 cards
        last_three_indices = [card.index for card in cards[1:]]
        
        # Create all possible permutations to find the encoding
        sorted_indices = self.sort_three_cards(last_three_indices.copy())
        
        # Check which permutation matches the current arrangement
        arrangements = [
            [sorted_indices[0], sorted_indices[1], sorted_indices[2]],  # encode 1
            [sorted_indices[0], sorted_indices[2], sorted_indices[1]],  # encode 2
            [sorted_indices[1], sorted_indices[0], sorted_indices[2]],  # encode 3
            [sorted_indices[1], sorted_indices[2], sorted_indices[0]],  # encode 4
            [sorted_indices[2], sorted_indices[0], sorted_indices[1]],  # encode 5
            [sorted_indices[2], sorted_indices[1], sorted_indices[0]]   # encode 6
        ]
        
        encode_value = None
        for i, arr in enumerate(arrangements):
            if arr == last_three_indices:
                encode_value = i + 1
                break
        
        if encode_value is None:
            raise ValueError("Invalid card arrangement!")
        
        # Calculate hidden card number
        hidden_number = (hidden_number_base + encode_value) % 13
        hidden_index = hidden_number * 4 + hidden_suit
        
        hidden_card = deck[hidden_index]
        print(f"\nThe hidden card is: {hidden_card}")
        return hidden_card
    
    def automated_demo(self):
        """Run a complete automated demonstration."""
        print("=== CARD TRICK DEMONSTRATION ===\n")
        
        # Assistant phase
        result = self.assistant_phase()
        
        print("\n" + "="*50)
        
        # Magician phase (simulated)
        print("\nNow as the Magician, I will deduce the hidden card...")
        
        # Recreate the arrangement for magician
        first_card_index = deck.index(str(result['first_card']))
        hidden_suit = first_card_index % 4
        hidden_number_base = first_card_index // 4
        
        # Use the encode value to calculate hidden card
        hidden_number = (hidden_number_base + result['encode_value']) % 13
        hidden_index = hidden_number * 4 + hidden_suit
        
        calculated_hidden = deck[hidden_index]
        
        print(f"First card: {result['first_card']} (suit: {self.suit_names[result['first_card'].suit_name]})")
        print(f"Arrangement suggests encode value: {result['encode_value']}")
        print(f"Calculated hidden card: {calculated_hidden}")
        
        if str(result['hidden_card']) == calculated_hidden:
            print("✅ Success! The trick worked perfectly!")
        else:
            print("❌ Error! Something went wrong.")
        
        return result['hidden_card'], calculated_hidden

def main():
    """Main function to run the card trick."""
    trick = CardTrick()
    
    while True:
        print("\n" + "="*60)
        print("CARD MIND READING TRICK")
        print("="*60)
        print("1. Assistant: Hide a card and arrange the others")
        print("2. Magician: Guess the hidden card")
        print("3. Automated demonstration")
        print("4. Exit")
        
        choice = input("\nChoose an option (1-4): ").strip()
        
        if choice == '1':
            trick.assistant_phase()
        elif choice == '2':
            trick.magician_phase()
        elif choice == '3':
            trick.automated_demo()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
