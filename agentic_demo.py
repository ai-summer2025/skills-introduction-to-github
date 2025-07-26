#!/usr/bin/env python3
"""
Chennai Dining - Agentic AI System Demo
Standalone demonstration of autonomous AI agents making decisions
"""

import json
import random
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

@dataclass
class Restaurant:
    id: str
    name: str
    location: str
    cuisine_type: str
    rating: float
    price_range: str
    specialties: List[str]
    capacity: int
    available_times: List[str]
    features: List[str]
    reviews_count: int

@dataclass
class UserPreferences:
    cuisine_preference: Optional[str] = None
    location_preference: Optional[str] = None
    budget: Optional[str] = None
    dietary_restrictions: List[str] = None
    occasion: Optional[str] = None
    group_size: Optional[int] = None
    preferred_time: Optional[str] = None
    ambiance_preference: Optional[str] = None

@dataclass
class BookingRequest:
    user_id: str
    message: str
    preferences: UserPreferences
    timestamp: datetime.datetime

@dataclass
class BookingResult:
    success: bool
    restaurant: Optional[Restaurant]
    booking_id: Optional[str]
    confirmation_details: Dict[str, Any]
    alternative_suggestions: List[Restaurant]
    agent_reasoning: str

class Agent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str, goal: str):
        self.name = name
        self.goal = goal
        self.memory = []
        self.learning_data = {}
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        pass
    
    def learn_from_interaction(self, interaction_data: Dict):
        """Agent learns from each interaction"""
        self.memory.append(interaction_data)
        self.update_learning_model(interaction_data)
    
    def update_learning_model(self, data: Dict):
        """Update agent's learning model based on user interactions"""
        for key, value in data.items():
            if key not in self.learning_data:
                self.learning_data[key] = []
            self.learning_data[key].append(value)

class RecommendationAgent(Agent):
    """AI Agent that autonomously recommends restaurants"""
    
    def __init__(self):
        super().__init__(
            name="RestaurantRecommendationAgent",
            goal="Find the perfect restaurant match using AI reasoning"
        )
        self.restaurants_db = self._initialize_restaurants()
    
    def _initialize_restaurants(self) -> List[Restaurant]:
        return [
            Restaurant(
                id="southern_spice", name="Southern Spice", location="T. Nagar",
                cuisine_type="South Indian", rating=4.5, price_range="mid-high",
                specialties=["Dosa varieties", "Filter coffee", "Sambar"],
                capacity=80, available_times=["12:00", "19:00", "20:00"],
                features=["air_conditioned", "family_friendly", "parking"], reviews_count=120
            ),
            Restaurant(
                id="chettinad_palace", name="Chettinad Palace", location="Adyar",
                cuisine_type="Chettinad", rating=4.8, price_range="high",
                specialties=["Chettinad Chicken", "Pepper Mutton", "Appam"],
                capacity=60, available_times=["12:00", "19:00", "21:00"],
                features=["authentic_decor", "spicy_food", "heritage_recipes"], reviews_count=200
            ),
            Restaurant(
                id="coastal_kitchen", name="Coastal Kitchen", location="Marina Beach",
                cuisine_type="Seafood", rating=4.2, price_range="mid",
                specialties=["Fish Curry", "Prawn Masala", "Crab Roast"],
                capacity=100, available_times=["12:30", "19:30", "20:30"],
                features=["sea_view", "fresh_seafood", "outdoor_seating"], reviews_count=85
            )
        ]
    
    def process(self, user_preferences: UserPreferences) -> List[Restaurant]:
        """AI agent autonomously analyzes and recommends restaurants"""
        print(f"🧠 {self.name} is thinking...")
        
        # AI Step 1: Analyze user context
        motivation = self._ai_infer_dining_motivation(user_preferences)
        print(f"   📊 AI Analysis: Dining motivation = {motivation}")
        
        # AI Step 2: Intelligent filtering
        candidates = self._ai_intelligent_filter(user_preferences)
        print(f"   🔍 AI Filtering: Found {len(candidates)} suitable restaurants")
        
        # AI Step 3: Autonomous ranking
        ranked = self._ai_ranking_algorithm(candidates, user_preferences)
        print(f"   🎯 AI Ranking: Applied multi-factor scoring algorithm")
        
        # AI Step 4: Learn from this decision
        self._learn_from_recommendation(user_preferences, ranked)
        
        return ranked[:3]
    
    def _ai_infer_dining_motivation(self, preferences: UserPreferences) -> str:
        """AI autonomously infers the purpose of dining"""
        if preferences.occasion and "anniversary" in preferences.occasion.lower():
            return "romantic_celebration"
        elif preferences.group_size and preferences.group_size > 6:
            return "group_gathering"
        elif preferences.occasion and "business" in preferences.occasion.lower():
            return "professional_meeting"
        return "casual_dining"
    
    def _ai_intelligent_filter(self, preferences: UserPreferences) -> List[Restaurant]:
        """AI applies intelligent filtering beyond simple matching"""
        candidates = self.restaurants_db.copy()
        
        # AI cuisine matching with fuzzy logic
        if preferences.cuisine_preference:
            candidates = [r for r in candidates if self._ai_cuisine_matches(r, preferences.cuisine_preference)]
        
        # AI location intelligence
        if preferences.location_preference:
            candidates = [r for r in candidates if preferences.location_preference.lower() in r.location.lower()]
        
        # AI capacity optimization
        if preferences.group_size:
            candidates = [r for r in candidates if r.capacity >= preferences.group_size * 2]
        
        return candidates
    
    def _ai_cuisine_matches(self, restaurant: Restaurant, preference: str) -> bool:
        """AI determines cuisine compatibility using fuzzy matching"""
        pref_lower = preference.lower()
        cuisine_lower = restaurant.cuisine_type.lower()
        
        # Direct match
        if pref_lower in cuisine_lower or cuisine_lower in pref_lower:
            return True
        
        # AI semantic matching
        if "spicy" in pref_lower and "chettinad" in cuisine_lower:
            return True
        if "traditional" in pref_lower and "south indian" in cuisine_lower:
            return True
        if "seafood" in pref_lower and restaurant.id == "coastal_kitchen":
            return True
            
        return False
    
    def _ai_ranking_algorithm(self, restaurants: List[Restaurant], preferences: UserPreferences) -> List[Restaurant]:
        """Advanced AI ranking with multiple factors"""
        scored_restaurants = []
        
        for restaurant in restaurants:
            score = restaurant.rating * 20  # Base score
            
            # AI contextual bonuses
            motivation = self._ai_infer_dining_motivation(preferences)
            if motivation == "romantic_celebration" and restaurant.price_range == "high":
                score += 30
            elif motivation == "group_gathering" and restaurant.capacity > 80:
                score += 25
            
            # AI budget compatibility
            if preferences.budget:
                if "budget" in preferences.budget.lower() and "low" in restaurant.price_range:
                    score += 20
                elif "luxury" in preferences.budget.lower() and "high" in restaurant.price_range:
                    score += 20
            
            # Add AI randomness for diversity
            score += random.uniform(-5, 5)
            
            scored_restaurants.append((restaurant, score))
        
        # Sort by AI-calculated score
        scored_restaurants.sort(key=lambda x: x[1], reverse=True)
        return [restaurant for restaurant, score in scored_restaurants]
    
    def _learn_from_recommendation(self, preferences: UserPreferences, recommendations: List[Restaurant]):
        """Agent learns from each recommendation"""
        learning_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "preferences": asdict(preferences),
            "recommendations": [r.id for r in recommendations]
        }
        self.learn_from_interaction(learning_data)

class BookingAgent(Agent):
    """AI Agent that autonomously handles bookings"""
    
    def __init__(self):
        super().__init__(
            name="BookingManagementAgent",
            goal="Successfully complete bookings while optimizing satisfaction"
        )
        self.active_bookings = {}
        self.booking_counter = 1000
    
    def process(self, booking_request: BookingRequest, restaurant_recommendations: List[Restaurant]) -> BookingResult:
        """AI agent autonomously manages booking process"""
        print(f"🧠 {self.name} is deciding...")
        
        # AI Step 1: Select best restaurant autonomously
        selected_restaurant = self._ai_restaurant_selection(booking_request, restaurant_recommendations)
        print(f"   🎯 AI Decision: Selected {selected_restaurant.name}")
        
        # AI Step 2: Intelligent availability check
        availability = self._ai_availability_prediction(selected_restaurant, booking_request)
        print(f"   📊 AI Prediction: Availability = {availability['probability']:.1%}")
        
        # AI Step 3: Autonomous booking decision
        if availability["available"]:
            result = self._ai_complete_booking(selected_restaurant, booking_request, availability)
            print(f"   ✅ AI Success: Booking confirmed!")
        else:
            result = self._ai_find_alternatives(booking_request, restaurant_recommendations)
            print(f"   🔄 AI Adaptation: Found alternatives")
        
        # AI Step 4: Learn from this booking attempt
        self._learn_from_booking(booking_request, result)
        
        return result
    
    def _ai_restaurant_selection(self, request: BookingRequest, recommendations: List[Restaurant]) -> Restaurant:
        """AI autonomously selects best restaurant from options"""
        if not recommendations:
            return None
        
        best_restaurant = recommendations[0]
        best_score = 0
        
        for restaurant in recommendations:
            # AI multi-factor scoring
            score = restaurant.rating * 0.4
            score += self._ai_predict_availability(restaurant, request) * 0.3
            score += self._ai_predict_satisfaction(restaurant, request) * 0.3
            
            if score > best_score:
                best_score = score
                best_restaurant = restaurant
        
        return best_restaurant
    
    def _ai_predict_availability(self, restaurant: Restaurant, request: BookingRequest) -> float:
        """AI predicts availability probability"""
        base_prob = 0.7
        
        # AI adjusts based on capacity vs group size
        if request.preferences.group_size:
            capacity_ratio = restaurant.capacity / request.preferences.group_size
            if capacity_ratio > 10:
                base_prob += 0.2
            elif capacity_ratio < 3:
                base_prob -= 0.3
        
        return max(0.1, min(1.0, base_prob))
    
    def _ai_predict_satisfaction(self, restaurant: Restaurant, request: BookingRequest) -> float:
        """AI predicts user satisfaction"""
        satisfaction = restaurant.rating / 5.0
        
        # AI context matching
        if request.preferences.cuisine_preference:
            if request.preferences.cuisine_preference.lower() in restaurant.cuisine_type.lower():
                satisfaction += 0.2
        
        return min(1.0, satisfaction)
    
    def _ai_availability_prediction(self, restaurant: Restaurant, request: BookingRequest) -> Dict:
        """AI performs intelligent availability prediction"""
        probability = self._ai_predict_availability(restaurant, request)
        is_available = random.random() < probability
        
        return {
            "available": is_available,
            "probability": probability,
            "confidence": probability if is_available else 1 - probability,
            "reasoning": f"AI predicted {probability:.1%} availability based on capacity and demand patterns"
        }
    
    def _ai_complete_booking(self, restaurant: Restaurant, request: BookingRequest, availability: Dict) -> BookingResult:
        """AI completes booking with autonomous decision making"""
        booking_id = f"CHN{self.booking_counter}"
        self.booking_counter += 1
        
        # AI generates optimal booking details
        booking_details = {
            "booking_id": booking_id,
            "restaurant": restaurant.name,
            "location": restaurant.location,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "time": self._ai_select_optimal_time(restaurant, request),
            "guests": request.preferences.group_size or 2,
            "user_id": request.user_id,
            "special_requests": self._ai_generate_special_requests(request, restaurant),
            "ai_confidence": availability["confidence"]
        }
        
        self.active_bookings[booking_id] = booking_details
        
        return BookingResult(
            success=True,
            restaurant=restaurant,
            booking_id=booking_id,
            confirmation_details=booking_details,
            alternative_suggestions=[],
            agent_reasoning=f"AI successfully booked {restaurant.name} with {availability['confidence']:.1%} confidence"
        )
    
    def _ai_select_optimal_time(self, restaurant: Restaurant, request: BookingRequest) -> str:
        """AI selects optimal time slot"""
        if request.preferences.preferred_time and request.preferences.preferred_time in restaurant.available_times:
            return request.preferences.preferred_time
        
        # AI selects based on group size
        if request.preferences.group_size and request.preferences.group_size > 6:
            return restaurant.available_times[0]  # Earlier for large groups
        
        return restaurant.available_times[len(restaurant.available_times)//2]  # Middle slot
    
    def _ai_generate_special_requests(self, request: BookingRequest, restaurant: Restaurant) -> List[str]:
        """AI autonomously generates special requests"""
        requests = []
        
        if request.preferences.occasion:
            occasion = request.preferences.occasion.lower()
            if "anniversary" in occasion:
                requests.extend(["Romantic corner table", "Special dessert arrangement"])
            elif "birthday" in occasion:
                requests.extend(["Birthday setup", "Cake arrangement"])
        
        if request.preferences.group_size and request.preferences.group_size > 6:
            requests.append("Large table arrangement")
        
        return requests
    
    def _ai_find_alternatives(self, request: BookingRequest, recommendations: List[Restaurant]) -> BookingResult:
        """AI autonomously finds alternatives when booking fails"""
        alternatives = []
        
        for restaurant in recommendations[1:]:  # Skip first one that failed
            availability = self._ai_availability_prediction(restaurant, request)
            if availability["available"]:
                alternatives.append(restaurant)
            if len(alternatives) >= 2:
                break
        
        return BookingResult(
            success=False,
            restaurant=None,
            booking_id=None,
            confirmation_details={},
            alternative_suggestions=alternatives,
            agent_reasoning=f"AI found {len(alternatives)} alternatives with good availability"
        )
    
    def _learn_from_booking(self, request: BookingRequest, result: BookingResult):
        """Agent learns from booking attempt"""
        learning_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "booking_success": result.success,
            "reasoning": result.agent_reasoning
        }
        self.learn_from_interaction(learning_data)

class CustomerServiceAgent(Agent):
    """AI Agent that processes natural language"""
    
    def __init__(self):
        super().__init__(
            name="CustomerServiceAgent",
            goal="Understand user intent and provide personalized responses"
        )
        self.conversation_memory = {}
    
    def process(self, user_message: str, user_id: str) -> Dict:
        """AI processes natural language autonomously"""
        print(f"🧠 {self.name} is understanding...")
        
        # AI Step 1: Analyze intent
        intent = self._ai_analyze_intent(user_message)
        print(f"   🎯 AI Intent Detection: {intent['primary_intent']}")
        
        # AI Step 2: Extract preferences
        preferences = self._ai_extract_preferences(user_message)
        print(f"   📊 AI Preference Extraction: {len([p for p in preferences.__dict__.values() if p])} preferences found")
        
        # AI Step 3: Generate response
        response = self._ai_generate_response(intent, preferences, user_id)
        print(f"   💬 AI Response Generation: Personalized message created")
        
        # AI Step 4: Update memory
        self._ai_update_memory(user_id, user_message, response)
        
        return {
            "intent": intent,
            "extracted_preferences": preferences,
            "response": response
        }
    
    def _ai_analyze_intent(self, message: str) -> Dict:
        """AI analyzes user intent from natural language"""
        message_lower = message.lower()
        
        intents = {
            "book_table": ["book", "reserve", "table", "booking", "reservation"],
            "ask_recommendation": ["recommend", "suggest", "best", "good"],
            "greeting": ["hello", "hi", "hey"]
        }
        
        detected_intents = []
        for intent, keywords in intents.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            if matches > 0:
                detected_intents.append((intent, matches))
        
        primary_intent = max(detected_intents, key=lambda x: x[1])[0] if detected_intents else "general_inquiry"
        
        return {
            "primary_intent": primary_intent,
            "confidence": len(detected_intents) / len(intents),
            "sentiment": self._ai_analyze_sentiment(message)
        }
    
    def _ai_analyze_sentiment(self, message: str) -> str:
        """AI analyzes sentiment"""
        positive_words = ["great", "excellent", "wonderful", "amazing", "love"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst"]
        
        message_lower = message.lower()
        positive_score = sum(1 for word in positive_words if word in message_lower)
        negative_score = sum(1 for word in negative_words if word in message_lower)
        
        if positive_score > negative_score:
            return "positive"
        elif negative_score > positive_score:
            return "negative"
        return "neutral"
    
    def _ai_extract_preferences(self, message: str) -> UserPreferences:
        """AI extracts preferences from natural language"""
        message_lower = message.lower()
        
        # AI extracts group size
        import re
        group_size = None
        for pattern in [r"(\d+)\s*people", r"(\d+)\s*guests", r"party\s*of\s*(\d+)"]:
            match = re.search(pattern, message_lower)
            if match:
                group_size = int(match.group(1))
                break
        
        # AI extracts cuisine
        cuisine_preference = None
        if any(word in message_lower for word in ["south indian", "dosa", "traditional"]):
            cuisine_preference = "South Indian"
        elif any(word in message_lower for word in ["chettinad", "spicy"]):
            cuisine_preference = "Chettinad"
        elif any(word in message_lower for word in ["seafood", "fish"]):
            cuisine_preference = "Seafood"
        
        # AI extracts occasion
        occasion = None
        if "anniversary" in message_lower:
            occasion = "anniversary"
        elif "birthday" in message_lower:
            occasion = "birthday"
        elif "business" in message_lower:
            occasion = "business"
        
        # AI extracts location
        location_preference = None
        locations = ["T. Nagar", "Adyar", "Marina Beach", "Mylapore"]
        for location in locations:
            if location.lower() in message_lower:
                location_preference = location
                break
        
        return UserPreferences(
            cuisine_preference=cuisine_preference,
            location_preference=location_preference,
            group_size=group_size,
            occasion=occasion
        )
    
    def _ai_generate_response(self, intent: Dict, preferences: UserPreferences, user_id: str) -> str:
        """AI generates personalized response"""
        primary_intent = intent["primary_intent"]
        sentiment = intent["sentiment"]
        
        # AI personalizes greeting
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            greeting = "Good morning!"
        elif current_hour < 17:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        
        if sentiment == "positive":
            greeting += " I'm excited to help you!"
        
        # AI generates intent-specific response
        if primary_intent == "book_table":
            response = "I'd be happy to help you book a table."
            if preferences.group_size:
                response += f" I see you need a table for {preferences.group_size} people."
            if preferences.occasion:
                response += f" For your {preferences.occasion}, I'll find the perfect spot."
        elif primary_intent == "ask_recommendation":
            response = "I'd love to recommend some amazing restaurants!"
            if preferences.cuisine_preference:
                response += f" Since you're interested in {preferences.cuisine_preference}, I have great options."
        else:
            response = "Welcome to Chennai Dining! How can I help you today?"
        
        return f"{greeting} {response}"
    
    def _ai_update_memory(self, user_id: str, user_message: str, response: str):
        """AI updates conversation memory"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        self.conversation_memory[user_id].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": response
        })

class AgenticBookingSystem:
    """Multi-Agent System Orchestrator"""
    
    def __init__(self):
        self.recommendation_agent = RecommendationAgent()
        self.booking_agent = BookingAgent()
        self.customer_service_agent = CustomerServiceAgent()
        self.total_interactions = 0
        self.successful_bookings = 0
    
    def process_user_request(self, user_message: str, user_id: str = None) -> Dict:
        """Main entry point - all agents work together autonomously"""
        
        if not user_id:
            user_id = f"user_{random.randint(1000, 9999)}"
        
        self.total_interactions += 1
        
        print(f"\n🤖 AGENTIC AI SYSTEM PROCESSING REQUEST")
        print(f"👤 User: {user_message}")
        print(f"🆔 User ID: {user_id}")
        print("=" * 50)
        
        # Agent 1: Customer Service processes natural language
        cs_result = self.customer_service_agent.process(user_message, user_id)
        
        # Agent coordination: If booking/recommendation intent detected
        if cs_result["intent"]["primary_intent"] in ["book_table", "ask_recommendation"]:
            
            # Agent 2: Recommendation Agent finds restaurants
            print(f"\n🔄 AGENT COORDINATION: Engaging Recommendation Agent")
            recommendations = self.recommendation_agent.process(cs_result["extracted_preferences"])
            
            # Agent 3: If booking intent, Booking Agent handles reservation
            if cs_result["intent"]["primary_intent"] == "book_table" and recommendations:
                print(f"\n🔄 AGENT COORDINATION: Engaging Booking Agent")
                
                booking_request = BookingRequest(
                    user_id=user_id,
                    message=user_message,
                    preferences=cs_result["extracted_preferences"],
                    timestamp=datetime.datetime.now()
                )
                
                booking_result = self.booking_agent.process(booking_request, recommendations)
                
                if booking_result.success:
                    self.successful_bookings += 1
                
                return self._format_booking_response(cs_result, recommendations, booking_result)
            else:
                return self._format_recommendation_response(cs_result, recommendations)
        else:
            return self._format_general_response(cs_result)
    
    def _format_booking_response(self, cs_result: Dict, recommendations: List[Restaurant], booking_result: BookingResult) -> Dict:
        """Format complete booking response"""
        
        print(f"\n📋 FINAL RESULT: Booking Response")
        print(f"✅ Success: {booking_result.success}")
        if booking_result.success:
            print(f"🏪 Restaurant: {booking_result.restaurant.name}")
            print(f"🆔 Booking ID: {booking_result.booking_id}")
        else:
            print(f"🔄 Alternatives: {len(booking_result.alternative_suggestions)} options")
        
        return {
            "type": "booking_response",
            "ai_response": cs_result["response"],
            "booking_success": booking_result.success,
            "booking_id": booking_result.booking_id,
            "restaurant": booking_result.restaurant.name if booking_result.restaurant else None,
            "confirmation_details": booking_result.confirmation_details,
            "recommendations": [{"name": r.name, "location": r.location, "rating": r.rating} for r in recommendations],
            "alternatives": [{"name": r.name, "location": r.location} for r in booking_result.alternative_suggestions],
            "agent_reasoning": booking_result.agent_reasoning
        }
    
    def _format_recommendation_response(self, cs_result: Dict, recommendations: List[Restaurant]) -> Dict:
        """Format recommendation response"""
        
        print(f"\n📋 FINAL RESULT: Recommendation Response")
        print(f"🍽️ Recommendations: {len(recommendations)} restaurants")
        for i, r in enumerate(recommendations[:2], 1):
            print(f"   {i}. {r.name} ({r.location}) - {r.rating}⭐")
        
        return {
            "type": "recommendation_response",
            "ai_response": cs_result["response"],
            "recommendations": [
                {
                    "name": r.name,
                    "location": r.location,
                    "cuisine": r.cuisine_type,
                    "rating": r.rating,
                    "specialties": r.specialties
                } for r in recommendations
            ]
        }
    
    def _format_general_response(self, cs_result: Dict) -> Dict:
        """Format general response"""
        
        print(f"\n📋 FINAL RESULT: General Response")
        print(f"💬 Intent: {cs_result['intent']['primary_intent']}")
        
        return {
            "type": "general_response",
            "ai_response": cs_result["response"],
            "intent_detected": cs_result["intent"]["primary_intent"]
        }
    
    def get_analytics(self) -> Dict:
        """Get system analytics"""
        return {
            "total_interactions": self.total_interactions,
            "successful_bookings": self.successful_bookings,
            "success_rate": (self.successful_bookings / max(1, self.total_interactions)) * 100,
            "agent_memory": {
                "recommendation_agent": len(self.recommendation_agent.memory),
                "booking_agent": len(self.booking_agent.memory),
                "customer_service_agent": len(self.customer_service_agent.memory)
            }
        }

def main():
    """Demonstrate the Agentic AI system"""
    
    print("🤖 CHENNAI DINING - AGENTIC AI SYSTEM DEMO")
    print("=" * 60)
    print("🧠 Multi-Agent System with Autonomous Decision Making")
    print("=" * 60)
    
    # Initialize the agentic system
    agentic_system = AgenticBookingSystem()
    
    # Test scenarios showing autonomous AI decision making
    test_scenarios = [
        "I want to book a table for 4 people tomorrow evening for my anniversary",
        "Can you recommend a good South Indian restaurant in T Nagar?",
        "I need a vegetarian restaurant for a business meeting, budget friendly",
        "Looking for the best seafood place near Marina Beach for 6 people",
        "What's the best restaurant for a birthday celebration?"
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"🎯 SCENARIO {i}: TESTING AUTONOMOUS AI AGENTS")
        print(f"{'='*60}")
        
        result = agentic_system.process_user_request(scenario)
        
        print(f"\n🎉 AUTONOMOUS AI AGENTS COMPLETED PROCESSING!")
        print(f"📊 Result Type: {result['type']}")
        print(f"💬 AI Response: {result['ai_response']}")
        
        if result['type'] == 'booking_response':
            if result['booking_success']:
                print(f"✅ AUTONOMOUS BOOKING SUCCESS!")
                print(f"🏪 Restaurant: {result['restaurant']}")
                print(f"🆔 Booking ID: {result['booking_id']}")
            else:
                print(f"🔄 AI FOUND ALTERNATIVES: {len(result.get('alternatives', []))} options")
        
        elif result['type'] == 'recommendation_response':
            print(f"🍽️ AI RECOMMENDATIONS: {len(result['recommendations'])} restaurants")
            for rec in result['recommendations'][:2]:
                print(f"   • {rec['name']} ({rec['location']}) - {rec['rating']}⭐")
    
    # Show system analytics
    print(f"\n{'='*60}")
    print(f"📊 AGENTIC AI SYSTEM ANALYTICS")
    print(f"{'='*60}")
    analytics = agentic_system.get_analytics()
    print(f"🔄 Total AI Interactions: {analytics['total_interactions']}")
    print(f"✅ Successful AI Bookings: {analytics['successful_bookings']}")
    print(f"📈 AI Success Rate: {analytics['success_rate']:.1f}%")
    print(f"🧠 Agent Memory Usage:")
    for agent, memory_count in analytics['agent_memory'].items():
        print(f"   • {agent}: {memory_count} interactions learned")
    
    print(f"\n🎉 AGENTIC AI DEMONSTRATION COMPLETE!")
    print(f"🤖 Key Features Demonstrated:")
    print(f"   ✅ Autonomous Decision Making")
    print(f"   ✅ Multi-Agent Coordination")
    print(f"   ✅ Natural Language Understanding")
    print(f"   ✅ Intelligent Reasoning")
    print(f"   ✅ Learning from Interactions")
    print(f"   ✅ Goal-Oriented Behavior")

if __name__ == "__main__":
    main()