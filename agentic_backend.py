#!/usr/bin/env python3
"""
Chennai Dining - Agentic AI Restaurant Booking System
Multi-Agent System with Autonomous Decision Making
"""

import json
import random
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import openai
import os

# Set up OpenAI (you would need to add your API key)
# openai.api_key = os.getenv("OPENAI_API_KEY")

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
        # Simulate learning by tracking patterns
        for key, value in data.items():
            if key not in self.learning_data:
                self.learning_data[key] = []
            self.learning_data[key].append(value)

class RecommendationAgent(Agent):
    """AI Agent that autonomously recommends restaurants based on user preferences"""
    
    def __init__(self):
        super().__init__(
            name="RestaurantRecommendationAgent",
            goal="Find the perfect restaurant match for each user based on their unique preferences and context"
        )
        self.restaurants_db = self._initialize_restaurants()
        self.user_behavior_patterns = {}
    
    def _initialize_restaurants(self) -> List[Restaurant]:
        """Initialize restaurant database with Chennai restaurants"""
        return [
            Restaurant(
                id="southern_spice",
                name="Southern Spice",
                location="T. Nagar",
                cuisine_type="South Indian",
                rating=4.5,
                price_range="mid-high",
                specialties=["Dosa varieties", "Filter coffee", "Sambar", "Rasam"],
                capacity=80,
                available_times=["12:00", "12:30", "13:00", "19:00", "19:30", "20:00"],
                features=["air_conditioned", "family_friendly", "parking", "traditional_decor"],
                reviews_count=120
            ),
            Restaurant(
                id="chettinad_palace",
                name="Chettinad Palace",
                location="Adyar",
                cuisine_type="Chettinad",
                rating=4.8,
                price_range="high",
                specialties=["Chettinad Chicken", "Pepper Mutton", "Kozhukattai", "Appam"],
                capacity=60,
                available_times=["12:00", "13:00", "19:00", "20:00", "21:00"],
                features=["authentic_decor", "spicy_food", "non_veg_specialty", "heritage_recipes"],
                reviews_count=200
            ),
            Restaurant(
                id="coastal_kitchen",
                name="Coastal Kitchen",
                location="Marina Beach",
                cuisine_type="Seafood",
                rating=4.2,
                price_range="mid",
                specialties=["Fish Curry", "Prawn Masala", "Crab Roast", "Karimeen Fry"],
                capacity=100,
                available_times=["12:30", "13:00", "13:30", "19:30", "20:00", "20:30"],
                features=["sea_view", "fresh_seafood", "casual_dining", "outdoor_seating"],
                reviews_count=85
            ),
            Restaurant(
                id="mylapore_mess",
                name="Mylapore Mess",
                location="Mylapore",
                cuisine_type="Traditional Tamil",
                rating=4.6,
                price_range="low-mid",
                specialties=["Meals", "Pongal", "Vadai", "Payasam"],
                capacity=50,
                available_times=["11:30", "12:00", "18:30", "19:00", "19:30"],
                features=["authentic_taste", "home_style", "vegetarian_friendly", "budget_friendly"],
                reviews_count=150
            ),
            Restaurant(
                id="namma_veedu",
                name="Namma Veedu",
                location="Velachery",
                cuisine_type="Home Style",
                rating=4.3,
                price_range="low",
                specialties=["Home Style Meals", "Comfort Food", "Grandmother Recipes"],
                capacity=40,
                available_times=["12:00", "19:00", "19:30", "20:00"],
                features=["home_atmosphere", "comfort_food", "family_recipes", "cozy"],
                reviews_count=95
            ),
            Restaurant(
                id="royal_feast",
                name="Royal Feast",
                location="Anna Nagar",
                cuisine_type="Multi-cuisine",
                rating=4.7,
                price_range="high",
                specialties=["Biryanis", "Tandoor", "Continental", "Desserts"],
                capacity=120,
                available_times=["12:00", "13:00", "19:00", "20:00", "21:00", "21:30"],
                features=["luxury_dining", "multi_cuisine", "party_venue", "valet_parking"],
                reviews_count=180
            )
        ]
    
    def process(self, user_preferences: UserPreferences) -> List[Restaurant]:
        """AI agent autonomously analyzes preferences and recommends restaurants"""
        reasoning_steps = []
        
        # Step 1: Analyze user preferences with AI reasoning
        preference_analysis = self._analyze_user_context(user_preferences)
        reasoning_steps.append(f"Analyzed user context: {preference_analysis}")
        
        # Step 2: Apply intelligent filtering
        filtered_restaurants = self._intelligent_filter(user_preferences)
        reasoning_steps.append(f"Applied intelligent filtering, found {len(filtered_restaurants)} matches")
        
        # Step 3: AI-powered ranking based on multiple factors
        ranked_restaurants = self._ai_ranking_algorithm(filtered_restaurants, user_preferences)
        reasoning_steps.append(f"Applied AI ranking algorithm")
        
        # Step 4: Learn from this interaction
        self._learn_from_recommendation(user_preferences, ranked_restaurants)
        
        # Store reasoning for transparency
        self.last_reasoning = reasoning_steps
        
        return ranked_restaurants[:3]  # Return top 3 recommendations
    
    def _analyze_user_context(self, preferences: UserPreferences) -> Dict:
        """AI analyzes the deeper context of user preferences"""
        context = {
            "dining_motivation": self._infer_dining_motivation(preferences),
            "budget_sensitivity": self._assess_budget_importance(preferences),
            "experience_priority": self._determine_experience_priority(preferences),
            "time_flexibility": self._evaluate_time_flexibility(preferences)
        }
        return context
    
    def _infer_dining_motivation(self, preferences: UserPreferences) -> str:
        """AI infers why the user wants to dine out"""
        if preferences.occasion:
            if "anniversary" in preferences.occasion.lower():
                return "romantic_celebration"
            elif "birthday" in preferences.occasion.lower():
                return "celebration"
            elif "business" in preferences.occasion.lower():
                return "professional_meeting"
        
        if preferences.group_size and preferences.group_size > 6:
            return "group_gathering"
        
        return "casual_dining"
    
    def _assess_budget_importance(self, preferences: UserPreferences) -> float:
        """AI assesses how important budget is to the user"""
        if preferences.budget:
            if "budget" in preferences.budget.lower() or "cheap" in preferences.budget.lower():
                return 0.9  # High importance
            elif "luxury" in preferences.budget.lower() or "expensive" in preferences.budget.lower():
                return 0.1  # Low importance
        return 0.5  # Medium importance
    
    def _determine_experience_priority(self, preferences: UserPreferences) -> str:
        """AI determines what kind of experience the user prioritizes"""
        if preferences.ambiance_preference:
            return preferences.ambiance_preference
        
        motivation = self._infer_dining_motivation(preferences)
        if motivation == "romantic_celebration":
            return "intimate_ambiance"
        elif motivation == "professional_meeting":
            return "quiet_professional"
        elif motivation == "group_gathering":
            return "spacious_lively"
        
        return "balanced_experience"
    
    def _evaluate_time_flexibility(self, preferences: UserPreferences) -> float:
        """AI evaluates how flexible the user is with timing"""
        if preferences.preferred_time:
            return 0.3  # Low flexibility if specific time mentioned
        return 0.8  # High flexibility if no specific time
    
    def _intelligent_filter(self, preferences: UserPreferences) -> List[Restaurant]:
        """AI applies intelligent filtering beyond basic criteria"""
        candidates = self.restaurants_db.copy()
        
        # Cuisine preference with AI reasoning
        if preferences.cuisine_preference:
            candidates = [r for r in candidates if self._cuisine_matches(r, preferences.cuisine_preference)]
        
        # Location intelligence - consider traffic, distance, etc.
        if preferences.location_preference:
            candidates = self._apply_location_intelligence(candidates, preferences.location_preference)
        
        # Dietary restrictions with smart matching
        if preferences.dietary_restrictions:
            candidates = self._smart_dietary_filter(candidates, preferences.dietary_restrictions)
        
        # Group size optimization
        if preferences.group_size:
            candidates = self._optimize_for_group_size(candidates, preferences.group_size)
        
        return candidates
    
    def _cuisine_matches(self, restaurant: Restaurant, preference: str) -> bool:
        """AI determines if cuisine matches user preference (fuzzy matching)"""
        preference_lower = preference.lower()
        cuisine_lower = restaurant.cuisine_type.lower()
        
        # Direct match
        if preference_lower in cuisine_lower or cuisine_lower in preference_lower:
            return True
        
        # Smart matching - AI understands related cuisines
        related_cuisines = {
            "spicy": ["chettinad", "south indian"],
            "traditional": ["traditional tamil", "south indian", "home style"],
            "seafood": ["coastal", "fish"],
            "vegetarian": ["south indian", "traditional tamil", "home style"],
            "authentic": ["chettinad", "traditional tamil", "home style"]
        }
        
        for key, cuisines in related_cuisines.items():
            if key in preference_lower and any(c in cuisine_lower for c in cuisines):
                return True
        
        return False
    
    def _apply_location_intelligence(self, restaurants: List[Restaurant], preference: str) -> List[Restaurant]:
        """AI considers location factors beyond just matching"""
        # Simulate AI reasoning about locations
        location_insights = {
            "central": ["T. Nagar", "Anna Nagar"],
            "beach": ["Marina Beach"],
            "traditional": ["Mylapore"],
            "convenient": ["Velachery", "Adyar"]
        }
        
        preference_lower = preference.lower()
        
        for insight, locations in location_insights.items():
            if insight in preference_lower:
                return [r for r in restaurants if r.location in locations]
        
        # If no specific insight, return restaurants close to preference
        return [r for r in restaurants if preference.lower() in r.location.lower()]
    
    def _smart_dietary_filter(self, restaurants: List[Restaurant], restrictions: List[str]) -> List[Restaurant]:
        """AI applies smart filtering for dietary restrictions"""
        filtered = []
        
        for restaurant in restaurants:
            is_suitable = True
            
            for restriction in restrictions:
                restriction_lower = restriction.lower()
                
                if "vegetarian" in restriction_lower or "veg" in restriction_lower:
                    if "vegetarian_friendly" not in restaurant.features and "non_veg_specialty" in restaurant.features:
                        is_suitable = False
                        break
                
                elif "spicy" in restriction_lower:
                    if restaurant.cuisine_type == "Chettinad":  # Known for spicy food
                        is_suitable = False
                        break
            
            if is_suitable:
                filtered.append(restaurant)
        
        return filtered
    
    def _optimize_for_group_size(self, restaurants: List[Restaurant], group_size: int) -> List[Restaurant]:
        """AI optimizes restaurant selection based on group size"""
        suitable = []
        
        for restaurant in restaurants:
            # AI reasoning about capacity vs group size
            capacity_ratio = restaurant.capacity / group_size
            
            if capacity_ratio >= 2:  # Restaurant can comfortably accommodate
                suitable.append(restaurant)
            elif capacity_ratio >= 1.5 and group_size <= 8:  # Acceptable for smaller groups
                suitable.append(restaurant)
        
        return suitable if suitable else restaurants  # Fallback to all if none suitable
    
    def _ai_ranking_algorithm(self, restaurants: List[Restaurant], preferences: UserPreferences) -> List[Restaurant]:
        """Advanced AI ranking algorithm considering multiple factors"""
        scored_restaurants = []
        
        for restaurant in restaurants:
            score = 0
            
            # Base rating score
            score += restaurant.rating * 20
            
            # AI-powered contextual scoring
            score += self._calculate_context_score(restaurant, preferences)
            score += self._calculate_experience_match_score(restaurant, preferences)
            score += self._calculate_budget_compatibility_score(restaurant, preferences)
            score += self._calculate_time_availability_score(restaurant, preferences)
            
            # Add some AI randomness for diversity
            score += random.uniform(-5, 5)
            
            scored_restaurants.append((restaurant, score))
        
        # Sort by score (highest first)
        scored_restaurants.sort(key=lambda x: x[1], reverse=True)
        
        return [restaurant for restaurant, score in scored_restaurants]
    
    def _calculate_context_score(self, restaurant: Restaurant, preferences: UserPreferences) -> float:
        """AI calculates how well restaurant matches the dining context"""
        score = 0
        
        motivation = self._infer_dining_motivation(preferences)
        
        if motivation == "romantic_celebration":
            if "luxury_dining" in restaurant.features or restaurant.price_range == "high":
                score += 30
            if restaurant.capacity < 80:  # More intimate
                score += 15
        
        elif motivation == "professional_meeting":
            if "air_conditioned" in restaurant.features:
                score += 20
            if restaurant.location in ["Anna Nagar", "T. Nagar"]:  # Business areas
                score += 15
        
        elif motivation == "group_gathering":
            if restaurant.capacity > 80:
                score += 25
            if "party_venue" in restaurant.features:
                score += 20
        
        return score
    
    def _calculate_experience_match_score(self, restaurant: Restaurant, preferences: UserPreferences) -> float:
        """AI scores based on experience matching"""
        score = 0
        
        experience_priority = self._determine_experience_priority(preferences)
        
        if experience_priority == "intimate_ambiance":
            if restaurant.capacity < 60:
                score += 20
            if "traditional_decor" in restaurant.features or "authentic_decor" in restaurant.features:
                score += 15
        
        elif experience_priority == "authentic_taste":
            if "authentic_taste" in restaurant.features or "heritage_recipes" in restaurant.features:
                score += 25
            if restaurant.cuisine_type in ["Chettinad", "Traditional Tamil"]:
                score += 15
        
        return score
    
    def _calculate_budget_compatibility_score(self, restaurant: Restaurant, preferences: UserPreferences) -> float:
        """AI calculates budget compatibility"""
        if not preferences.budget:
            return 0
        
        budget_importance = self._assess_budget_importance(preferences)
        
        if budget_importance > 0.7:  # Budget is important
            if restaurant.price_range in ["low", "low-mid"]:
                return 25
            else:
                return -15
        
        elif budget_importance < 0.3:  # Budget is not important
            if restaurant.price_range == "high":
                return 15
        
        return 0
    
    def _calculate_time_availability_score(self, restaurant: Restaurant, preferences: UserPreferences) -> float:
        """AI scores based on time availability"""
        if not preferences.preferred_time:
            return 0
        
        if preferences.preferred_time in restaurant.available_times:
            return 20
        
        # AI finds close time matches
        preferred_hour = int(preferences.preferred_time.split(':')[0])
        available_hours = [int(time.split(':')[0]) for time in restaurant.available_times]
        
        closest_diff = min(abs(preferred_hour - hour) for hour in available_hours)
        
        if closest_diff <= 1:
            return 10
        elif closest_diff <= 2:
            return 5
        
        return 0
    
    def _learn_from_recommendation(self, preferences: UserPreferences, recommendations: List[Restaurant]):
        """Agent learns from each recommendation for future improvements"""
        learning_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "preferences": asdict(preferences),
            "recommendations": [r.id for r in recommendations],
            "reasoning": getattr(self, 'last_reasoning', [])
        }
        
        self.learn_from_interaction(learning_data)
    
    def get_reasoning_explanation(self) -> List[str]:
        """Returns the AI agent's reasoning process"""
        return getattr(self, 'last_reasoning', ["No reasoning available"])

class BookingAgent(Agent):
    """AI Agent that handles booking process and decision making"""
    
    def __init__(self):
        super().__init__(
            name="BookingManagementAgent",
            goal="Successfully complete restaurant bookings while optimizing user satisfaction"
        )
        self.active_bookings = {}
        self.booking_counter = 1000
    
    def process(self, booking_request: BookingRequest, restaurant_recommendations: List[Restaurant]) -> BookingResult:
        """AI agent autonomously manages the booking process"""
        
        # AI decides the best restaurant from recommendations
        selected_restaurant = self._ai_restaurant_selection(booking_request, restaurant_recommendations)
        
        # AI checks availability and makes autonomous decisions
        availability_result = self._intelligent_availability_check(selected_restaurant, booking_request)
        
        if availability_result["available"]:
            # AI completes the booking
            booking_result = self._complete_booking(selected_restaurant, booking_request, availability_result)
        else:
            # AI autonomously finds alternatives
            booking_result = self._find_alternatives(booking_request, restaurant_recommendations)
        
        # Learn from this booking attempt
        self._learn_from_booking(booking_request, booking_result)
        
        return booking_result
    
    def _ai_restaurant_selection(self, request: BookingRequest, recommendations: List[Restaurant]) -> Restaurant:
        """AI autonomously selects the best restaurant from recommendations"""
        if not recommendations:
            return None
        
        # AI reasoning for selection
        selection_factors = {
            "user_preferences_match": 0.4,
            "availability_likelihood": 0.3,
            "satisfaction_prediction": 0.2,
            "booking_success_history": 0.1
        }
        
        best_restaurant = recommendations[0]  # Start with top recommendation
        best_score = 0
        
        for restaurant in recommendations:
            score = 0
            
            # Factor 1: Preference matching (already done by recommendation agent)
            score += 0.4 * (restaurant.rating / 5.0)
            
            # Factor 2: Availability likelihood (AI predicts based on time and day)
            availability_prob = self._predict_availability(restaurant, request)
            score += 0.3 * availability_prob
            
            # Factor 3: Satisfaction prediction (AI predicts user satisfaction)
            satisfaction_prob = self._predict_user_satisfaction(restaurant, request)
            score += 0.2 * satisfaction_prob
            
            # Factor 4: Historical booking success
            success_rate = self._get_historical_success_rate(restaurant)
            score += 0.1 * success_rate
            
            if score > best_score:
                best_score = score
                best_restaurant = restaurant
        
        return best_restaurant
    
    def _predict_availability(self, restaurant: Restaurant, request: BookingRequest) -> float:
        """AI predicts likelihood of availability"""
        # Simulate AI prediction based on various factors
        base_probability = 0.7
        
        # Adjust based on restaurant capacity vs group size
        if request.preferences.group_size:
            capacity_ratio = restaurant.capacity / request.preferences.group_size
            if capacity_ratio > 10:
                base_probability += 0.2
            elif capacity_ratio < 3:
                base_probability -= 0.3
        
        # Adjust based on time (peak hours less likely)
        if request.preferences.preferred_time:
            hour = int(request.preferences.preferred_time.split(':')[0])
            if hour in [19, 20]:  # Peak dinner hours
                base_probability -= 0.2
            elif hour in [12, 13]:  # Peak lunch hours
                base_probability -= 0.1
        
        return max(0.1, min(1.0, base_probability))
    
    def _predict_user_satisfaction(self, restaurant: Restaurant, request: BookingRequest) -> float:
        """AI predicts user satisfaction based on various factors"""
        satisfaction_score = restaurant.rating / 5.0
        
        # Adjust based on preference matching
        if request.preferences.cuisine_preference:
            if request.preferences.cuisine_preference.lower() in restaurant.cuisine_type.lower():
                satisfaction_score += 0.2
        
        # Adjust based on occasion matching
        if request.preferences.occasion:
            occasion = request.preferences.occasion.lower()
            if "anniversary" in occasion and "luxury_dining" in restaurant.features:
                satisfaction_score += 0.3
            elif "birthday" in occasion and restaurant.capacity > 60:
                satisfaction_score += 0.2
        
        return min(1.0, satisfaction_score)
    
    def _get_historical_success_rate(self, restaurant: Restaurant) -> float:
        """AI retrieves historical booking success rate for restaurant"""
        # Simulate historical data
        success_rates = {
            "southern_spice": 0.85,
            "chettinad_palace": 0.90,
            "coastal_kitchen": 0.75,
            "mylapore_mess": 0.80,
            "namma_veedu": 0.95,
            "royal_feast": 0.70
        }
        
        return success_rates.get(restaurant.id, 0.8)
    
    def _intelligent_availability_check(self, restaurant: Restaurant, request: BookingRequest) -> Dict:
        """AI performs intelligent availability checking"""
        # Simulate availability check with AI reasoning
        availability_probability = self._predict_availability(restaurant, request)
        
        # AI makes decision based on probability
        is_available = random.random() < availability_probability
        
        if is_available:
            # AI selects best available time
            available_time = self._ai_time_selection(restaurant, request)
            return {
                "available": True,
                "confirmed_time": available_time,
                "confidence": availability_probability,
                "reasoning": f"High confidence booking available at {available_time}"
            }
        else:
            # AI suggests alternative times
            alternative_times = self._suggest_alternative_times(restaurant, request)
            return {
                "available": False,
                "alternative_times": alternative_times,
                "confidence": 1 - availability_probability,
                "reasoning": f"Preferred time not available, suggesting alternatives"
            }
    
    def _ai_time_selection(self, restaurant: Restaurant, request: BookingRequest) -> str:
        """AI autonomously selects the best available time"""
        if request.preferences.preferred_time and request.preferences.preferred_time in restaurant.available_times:
            return request.preferences.preferred_time
        
        # AI finds the closest match
        if request.preferences.preferred_time:
            preferred_hour = int(request.preferences.preferred_time.split(':')[0])
            available_times = restaurant.available_times
            
            closest_time = min(available_times, 
                             key=lambda t: abs(int(t.split(':')[0]) - preferred_hour))
            return closest_time
        
        # AI selects based on group size and occasion
        if request.preferences.group_size and request.preferences.group_size > 6:
            # Larger groups get earlier slots
            return restaurant.available_times[0]
        
        # Default to middle time slot
        return restaurant.available_times[len(restaurant.available_times)//2]
    
    def _suggest_alternative_times(self, restaurant: Restaurant, request: BookingRequest) -> List[str]:
        """AI suggests alternative times using intelligent reasoning"""
        alternatives = []
        
        # AI considers user flexibility
        flexibility = self._assess_user_flexibility(request)
        
        if flexibility > 0.7:  # High flexibility
            alternatives = restaurant.available_times[:3]
        elif flexibility > 0.4:  # Medium flexibility
            alternatives = restaurant.available_times[:2]
        else:  # Low flexibility
            alternatives = [restaurant.available_times[0]]
        
        return alternatives
    
    def _assess_user_flexibility(self, request: BookingRequest) -> float:
        """AI assesses how flexible the user is with time changes"""
        flexibility = 0.5  # Base flexibility
        
        # Business meetings are less flexible
        if request.preferences.occasion and "business" in request.preferences.occasion.lower():
            flexibility -= 0.3
        
        # Large groups are less flexible
        if request.preferences.group_size and request.preferences.group_size > 8:
            flexibility -= 0.2
        
        # Special occasions are less flexible
        if request.preferences.occasion and any(word in request.preferences.occasion.lower() 
                                              for word in ["anniversary", "birthday"]):
            flexibility -= 0.2
        
        return max(0.1, min(1.0, flexibility))
    
    def _complete_booking(self, restaurant: Restaurant, request: BookingRequest, availability: Dict) -> BookingResult:
        """AI completes the booking with autonomous decision making"""
        
        # Generate unique booking ID
        booking_id = f"CHN{self.booking_counter}"
        self.booking_counter += 1
        
        # AI creates comprehensive booking details
        booking_details = {
            "booking_id": booking_id,
            "restaurant": restaurant.name,
            "location": restaurant.location,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "time": availability["confirmed_time"],
            "guests": request.preferences.group_size or 2,
            "user_id": request.user_id,
            "special_requests": self._ai_generate_special_requests(request, restaurant),
            "estimated_duration": self._ai_estimate_duration(request, restaurant),
            "confirmation_sent": True,
            "agent_confidence": availability["confidence"]
        }
        
        # Store booking
        self.active_bookings[booking_id] = booking_details
        
        return BookingResult(
            success=True,
            restaurant=restaurant,
            booking_id=booking_id,
            confirmation_details=booking_details,
            alternative_suggestions=[],
            agent_reasoning=f"Successfully booked {restaurant.name} for {availability['confirmed_time']} with {availability['confidence']:.1%} confidence"
        )
    
    def _ai_generate_special_requests(self, request: BookingRequest, restaurant: Restaurant) -> List[str]:
        """AI autonomously generates special requests based on context"""
        special_requests = []
        
        # AI infers special needs
        if request.preferences.occasion:
            occasion = request.preferences.occasion.lower()
            if "anniversary" in occasion:
                special_requests.append("Request romantic corner table")
                special_requests.append("Special dessert arrangement")
            elif "birthday" in occasion:
                special_requests.append("Birthday cake arrangement")
                special_requests.append("Decoration setup")
        
        # AI considers group size
        if request.preferences.group_size and request.preferences.group_size > 6:
            special_requests.append("Large table arrangement")
            special_requests.append("Group seating preference")
        
        # AI handles dietary restrictions
        if request.preferences.dietary_restrictions:
            for restriction in request.preferences.dietary_restrictions:
                special_requests.append(f"Dietary requirement: {restriction}")
        
        return special_requests
    
    def _ai_estimate_duration(self, request: BookingRequest, restaurant: Restaurant) -> int:
        """AI estimates dining duration in minutes"""
        base_duration = 90  # Base 1.5 hours
        
        # Adjust based on occasion
        if request.preferences.occasion:
            occasion = request.preferences.occasion.lower()
            if "business" in occasion:
                base_duration = 60  # Shorter for business
            elif "anniversary" in occasion or "celebration" in occasion:
                base_duration = 120  # Longer for celebrations
        
        # Adjust based on group size
        if request.preferences.group_size:
            if request.preferences.group_size > 6:
                base_duration += 30  # Longer for large groups
        
        # Adjust based on restaurant type
        if restaurant.price_range == "high":
            base_duration += 30  # Fine dining takes longer
        elif restaurant.price_range == "low":
            base_duration -= 15  # Casual dining is quicker
        
        return base_duration
    
    def _find_alternatives(self, request: BookingRequest, recommendations: List[Restaurant]) -> BookingResult:
        """AI autonomously finds alternative solutions when booking fails"""
        
        alternatives = []
        reasoning_steps = []
        
        # Try other recommended restaurants
        for restaurant in recommendations[1:]:  # Skip the first one that failed
            availability = self._intelligent_availability_check(restaurant, request)
            if availability["available"]:
                alternatives.append(restaurant)
                reasoning_steps.append(f"Found availability at {restaurant.name}")
            
            if len(alternatives) >= 2:  # Limit alternatives
                break
        
        # If still no alternatives, AI suggests time changes
        if not alternatives and recommendations:
            primary_restaurant = recommendations[0]
            alternative_times = self._suggest_alternative_times(primary_restaurant, request)
            reasoning_steps.append(f"Suggesting alternative times at {primary_restaurant.name}")
            
            return BookingResult(
                success=False,
                restaurant=primary_restaurant,
                booking_id=None,
                confirmation_details={"alternative_times": alternative_times},
                alternative_suggestions=recommendations[1:3],
                agent_reasoning=f"Primary choice unavailable. Suggested times: {', '.join(alternative_times)}"
            )
        
        return BookingResult(
            success=False,
            restaurant=None,
            booking_id=None,
            confirmation_details={},
            alternative_suggestions=alternatives,
            agent_reasoning=f"Found {len(alternatives)} alternative restaurants: {', '.join([r.name for r in alternatives])}"
        )
    
    def _learn_from_booking(self, request: BookingRequest, result: BookingResult):
        """Agent learns from each booking attempt"""
        learning_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "booking_success": result.success,
            "user_preferences": asdict(request.preferences),
            "selected_restaurant": result.restaurant.id if result.restaurant else None,
            "reasoning": result.agent_reasoning
        }
        
        self.learn_from_interaction(learning_data)

class CustomerServiceAgent(Agent):
    """AI Agent that handles customer communication and natural language processing"""
    
    def __init__(self):
        super().__init__(
            name="CustomerServiceAgent",
            goal="Provide excellent customer service through natural language understanding and personalized responses"
        )
        self.conversation_memory = {}
    
    def process(self, user_message: str, user_id: str, context: Dict = None) -> Dict:
        """AI agent processes natural language and provides intelligent responses"""
        
        # AI analyzes user intent
        intent_analysis = self._analyze_user_intent(user_message)
        
        # AI extracts preferences from natural language
        extracted_preferences = self._extract_preferences_from_text(user_message)
        
        # AI generates personalized response
        response = self._generate_intelligent_response(intent_analysis, extracted_preferences, user_id)
        
        # AI updates conversation memory
        self._update_conversation_memory(user_id, user_message, response)
        
        return {
            "intent": intent_analysis,
            "extracted_preferences": extracted_preferences,
            "response": response,
            "conversation_state": self.conversation_memory.get(user_id, {})
        }
    
    def _analyze_user_intent(self, message: str) -> Dict:
        """AI analyzes user intent from natural language"""
        message_lower = message.lower()
        
        intents = {
            "book_table": ["book", "reserve", "table", "booking", "reservation"],
            "ask_recommendation": ["recommend", "suggest", "best", "good", "where"],
            "modify_booking": ["change", "modify", "update", "reschedule"],
            "cancel_booking": ["cancel", "delete", "remove"],
            "ask_info": ["info", "information", "details", "tell me", "what"],
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"]
        }
        
        detected_intents = []
        confidence_scores = {}
        
        for intent, keywords in intents.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            if matches > 0:
                confidence = matches / len(keywords)
                detected_intents.append(intent)
                confidence_scores[intent] = confidence
        
        # AI reasoning for primary intent
        if detected_intents:
            primary_intent = max(detected_intents, key=lambda x: confidence_scores[x])
        else:
            primary_intent = "general_inquiry"
        
        return {
            "primary_intent": primary_intent,
            "all_intents": detected_intents,
            "confidence_scores": confidence_scores,
            "message_analysis": self._analyze_message_sentiment(message)
        }
    
    def _analyze_message_sentiment(self, message: str) -> Dict:
        """AI analyzes sentiment and urgency of message"""
        message_lower = message.lower()
        
        # Positive indicators
        positive_words = ["great", "excellent", "wonderful", "amazing", "perfect", "love"]
        positive_score = sum(1 for word in positive_words if word in message_lower)
        
        # Negative indicators
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "horrible"]
        negative_score = sum(1 for word in negative_words if word in message_lower)
        
        # Urgency indicators
        urgency_words = ["urgent", "asap", "immediately", "now", "quick", "soon"]
        urgency_score = sum(1 for word in urgency_words if word in message_lower)
        
        return {
            "sentiment": "positive" if positive_score > negative_score else "negative" if negative_score > 0 else "neutral",
            "urgency": "high" if urgency_score > 0 else "normal",
            "politeness": "polite" if any(word in message_lower for word in ["please", "thank", "sorry"]) else "casual"
        }
    
    def _extract_preferences_from_text(self, message: str) -> UserPreferences:
        """AI extracts user preferences from natural language"""
        message_lower = message.lower()
        
        # Extract cuisine preferences
        cuisine_keywords = {
            "south indian": ["south indian", "dosa", "idli", "sambar", "traditional"],
            "chettinad": ["chettinad", "spicy", "pepper", "authentic"],
            "seafood": ["seafood", "fish", "prawn", "crab", "coastal"],
            "vegetarian": ["vegetarian", "veg", "no meat", "plant based"]
        }
        
        cuisine_preference = None
        for cuisine, keywords in cuisine_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                cuisine_preference = cuisine
                break
        
        # Extract location preferences
        location_keywords = {
            "T. Nagar": ["t nagar", "t.nagar", "tnagar", "central"],
            "Adyar": ["adyar", "south chennai"],
            "Marina Beach": ["marina", "beach", "seaside"],
            "Mylapore": ["mylapore", "traditional area"],
            "Velachery": ["velachery", "south"],
            "Anna Nagar": ["anna nagar", "north", "convenient"]
        }
        
        location_preference = None
        for location, keywords in location_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                location_preference = location
                break
        
        # Extract group size
        import re
        group_size = None
        group_patterns = [
            r"(\d+)\s*people",
            r"(\d+)\s*persons",
            r"(\d+)\s*guests",
            r"group\s*of\s*(\d+)",
            r"party\s*of\s*(\d+)"
        ]
        
        for pattern in group_patterns:
            match = re.search(pattern, message_lower)
            if match:
                group_size = int(match.group(1))
                break
        
        # Extract occasion
        occasion_keywords = {
            "anniversary": ["anniversary", "wedding anniversary"],
            "birthday": ["birthday", "bday", "birth day"],
            "business": ["business", "meeting", "work", "office"],
            "celebration": ["celebration", "party", "special occasion"],
            "romantic": ["romantic", "date", "couple"]
        }
        
        occasion = None
        for occ, keywords in occasion_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                occasion = occ
                break
        
        # Extract budget preferences
        budget = None
        if any(word in message_lower for word in ["budget", "cheap", "affordable", "inexpensive"]):
            budget = "budget-friendly"
        elif any(word in message_lower for word in ["expensive", "luxury", "fine dining", "premium"]):
            budget = "luxury"
        
        # Extract dietary restrictions
        dietary_restrictions = []
        diet_keywords = {
            "vegetarian": ["vegetarian", "veg only", "no meat"],
            "no spicy": ["not spicy", "mild", "no chili"],
            "gluten free": ["gluten free", "no wheat"],
            "vegan": ["vegan", "plant based"]
        }
        
        for restriction, keywords in diet_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                dietary_restrictions.append(restriction)
        
        return UserPreferences(
            cuisine_preference=cuisine_preference,
            location_preference=location_preference,
            group_size=group_size,
            occasion=occasion,
            budget=budget,
            dietary_restrictions=dietary_restrictions if dietary_restrictions else None
        )
    
    def _generate_intelligent_response(self, intent_analysis: Dict, preferences: UserPreferences, user_id: str) -> str:
        """AI generates personalized and contextual responses"""
        
        primary_intent = intent_analysis["primary_intent"]
        sentiment = intent_analysis["message_analysis"]["sentiment"]
        urgency = intent_analysis["message_analysis"]["urgency"]
        
        # AI personalizes greeting based on time and user history
        greeting = self._generate_contextual_greeting(user_id, sentiment, urgency)
        
        # AI generates intent-specific response
        if primary_intent == "book_table":
            response = self._generate_booking_response(preferences, urgency)
        elif primary_intent == "ask_recommendation":
            response = self._generate_recommendation_response(preferences)
        elif primary_intent == "ask_info":
            response = self._generate_info_response(preferences)
        elif primary_intent == "greeting":
            response = self._generate_friendly_response()
        else:
            response = self._generate_general_response(preferences)
        
        # AI adds personalized closing
        closing = self._generate_contextual_closing(sentiment, urgency)
        
        return f"{greeting} {response} {closing}"
    
    def _generate_contextual_greeting(self, user_id: str, sentiment: str, urgency: str) -> str:
        """AI generates contextual greeting"""
        current_hour = datetime.datetime.now().hour
        
        if urgency == "high":
            return "I'll help you right away!"
        
        if current_hour < 12:
            greeting = "Good morning!"
        elif current_hour < 17:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        
        if sentiment == "positive":
            return f"{greeting} I'm excited to help you with your dining plans!"
        elif sentiment == "negative":
            return f"{greeting} I'm here to help resolve any concerns and find you the perfect dining experience."
        else:
            return f"{greeting} Welcome to Chennai Dining!"
    
    def _generate_booking_response(self, preferences: UserPreferences, urgency: str) -> str:
        """AI generates booking-specific response"""
        if urgency == "high":
            response = "Let me quickly find you the best available options."
        else:
            response = "I'd be happy to help you book a table."
        
        # AI mentions recognized preferences
        recognized = []
        if preferences.cuisine_preference:
            recognized.append(f"{preferences.cuisine_preference} cuisine")
        if preferences.location_preference:
            recognized.append(f"{preferences.location_preference} area")
        if preferences.group_size:
            recognized.append(f"party of {preferences.group_size}")
        if preferences.occasion:
            recognized.append(f"{preferences.occasion} occasion")
        
        if recognized:
            response += f" I understand you're looking for {', '.join(recognized)}."
        
        response += " Let me check our best restaurants and find perfect matches for you."
        
        return response
    
    def _generate_recommendation_response(self, preferences: UserPreferences) -> str:
        """AI generates recommendation-specific response"""
        response = "I'd love to recommend some amazing restaurants in Chennai!"
        
        if preferences.cuisine_preference:
            response += f" Since you're interested in {preferences.cuisine_preference}, I have some fantastic options in mind."
        
        if preferences.occasion:
            response += f" For your {preferences.occasion}, I'll suggest places with the perfect ambiance."
        
        response += " Let me analyze your preferences and find the ideal dining spots."
        
        return response
    
    def _generate_info_response(self, preferences: UserPreferences) -> str:
        """AI generates information-specific response"""
        return "I'd be happy to provide information about our restaurants, booking process, or anything else you'd like to know about Chennai's dining scene."
    
    def _generate_friendly_response(self) -> str:
        """AI generates friendly response for greetings"""
        responses = [
            "Welcome to Chennai Dining! I'm your AI dining assistant, ready to help you discover amazing restaurants and book the perfect table.",
            "Hello! I'm here to help you find the best dining experiences in Chennai. What kind of cuisine are you in the mood for today?",
            "Hi there! Whether you're looking for traditional South Indian flavors or contemporary dining, I'll help you find the perfect restaurant."
        ]
        return random.choice(responses)
    
    def _generate_general_response(self, preferences: UserPreferences) -> str:
        """AI generates general response"""
        return "I'm here to help you with restaurant recommendations, table bookings, or any questions about Chennai's dining scene. How can I assist you today?"
    
    def _generate_contextual_closing(self, sentiment: str, urgency: str) -> str:
        """AI generates contextual closing"""
        if urgency == "high":
            return "I'll get this sorted for you immediately!"
        elif sentiment == "positive":
            return "I'm excited to help you have a wonderful dining experience!"
        else:
            return "Let me know if you need any additional information!"
    
    def _update_conversation_memory(self, user_id: str, user_message: str, response: str):
        """AI updates conversation memory for context"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = {
                "conversation_history": [],
                "user_preferences": {},
                "last_interaction": None
            }
        
        self.conversation_memory[user_id]["conversation_history"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": response
        })
        
        self.conversation_memory[user_id]["last_interaction"] = datetime.datetime.now()
        
        # Keep only last 10 interactions for memory efficiency
        if len(self.conversation_memory[user_id]["conversation_history"]) > 10:
            self.conversation_memory[user_id]["conversation_history"] = \
                self.conversation_memory[user_id]["conversation_history"][-10:]

class AgenticBookingSystem:
    """Main orchestrator for the multi-agent system"""
    
    def __init__(self):
        self.recommendation_agent = RecommendationAgent()
        self.booking_agent = BookingAgent()
        self.customer_service_agent = CustomerServiceAgent()
        self.system_memory = {
            "total_interactions": 0,
            "successful_bookings": 0,
            "user_satisfaction_scores": []
        }
    
    def process_user_request(self, user_message: str, user_id: str = None) -> Dict:
        """Main entry point for agentic system - all agents work together autonomously"""
        
        if not user_id:
            user_id = f"user_{random.randint(1000, 9999)}"
        
        self.system_memory["total_interactions"] += 1
        
        # Step 1: Customer Service Agent processes natural language
        cs_result = self.customer_service_agent.process(user_message, user_id)
        
        # Step 2: If booking intent detected, engage other agents
        if cs_result["intent"]["primary_intent"] in ["book_table", "ask_recommendation"]:
            
            # Create booking request
            booking_request = BookingRequest(
                user_id=user_id,
                message=user_message,
                preferences=cs_result["extracted_preferences"],
                timestamp=datetime.datetime.now()
            )
            
            # Step 3: Recommendation Agent autonomously finds best restaurants
            recommendations = self.recommendation_agent.process(booking_request.preferences)
            
            # Step 4: If booking intent, Booking Agent handles the reservation
            if cs_result["intent"]["primary_intent"] == "book_table" and recommendations:
                booking_result = self.booking_agent.process(booking_request, recommendations)
                
                if booking_result.success:
                    self.system_memory["successful_bookings"] += 1
                
                return self._format_booking_response(cs_result, recommendations, booking_result)
            
            else:
                # Just recommendations requested
                return self._format_recommendation_response(cs_result, recommendations)
        
        else:
            # General inquiry or other intent
            return self._format_general_response(cs_result)
    
    def _format_booking_response(self, cs_result: Dict, recommendations: List[Restaurant], booking_result: BookingResult) -> Dict:
        """Format complete booking response with all agent insights"""
        
        response = {
            "type": "booking_response",
            "ai_response": cs_result["response"],
            "booking_success": booking_result.success,
            "recommendations": [
                {
                    "id": r.id,
                    "name": r.name,
                    "location": r.location,
                    "cuisine": r.cuisine_type,
                    "rating": r.rating,
                    "price_range": r.price_range,
                    "specialties": r.specialties,
                    "features": r.features
                } for r in recommendations
            ],
            "agent_insights": {
                "recommendation_reasoning": self.recommendation_agent.get_reasoning_explanation(),
                "booking_reasoning": booking_result.agent_reasoning,
                "customer_service_analysis": cs_result["intent"]
            }
        }
        
        if booking_result.success:
            response["booking_confirmation"] = {
                "booking_id": booking_result.booking_id,
                "restaurant": {
                    "name": booking_result.restaurant.name,
                    "location": booking_result.restaurant.location,
                    "rating": booking_result.restaurant.rating
                },
                "details": booking_result.confirmation_details,
                "success_message": f"✅ Booking confirmed at {booking_result.restaurant.name}! Your booking ID is {booking_result.booking_id}."
            }
        else:
            response["alternatives"] = [
                {
                    "name": r.name,
                    "location": r.location,
                    "rating": r.rating,
                    "why_recommended": "Alternative option with good availability"
                } for r in booking_result.alternative_suggestions
            ]
            response["fallback_message"] = f"❌ Couldn't complete booking, but I found {len(booking_result.alternative_suggestions)} great alternatives!"
        
        return response
    
    def _format_recommendation_response(self, cs_result: Dict, recommendations: List[Restaurant]) -> Dict:
        """Format recommendation-only response"""
        
        return {
            "type": "recommendation_response",
            "ai_response": cs_result["response"],
            "recommendations": [
                {
                    "id": r.id,
                    "name": r.name,
                    "location": r.location,
                    "cuisine": r.cuisine_type,
                    "rating": r.rating,
                    "price_range": r.price_range,
                    "specialties": r.specialties[:3],  # Top 3 specialties
                    "why_recommended": f"Perfect match for {cs_result['extracted_preferences'].cuisine_preference or 'your preferences'}"
                } for r in recommendations
            ],
            "agent_insights": {
                "recommendation_reasoning": self.recommendation_agent.get_reasoning_explanation(),
                "customer_service_analysis": cs_result["intent"]
            },
            "next_step_suggestion": "Would you like me to book a table at any of these restaurants?"
        }
    
    def _format_general_response(self, cs_result: Dict) -> Dict:
        """Format general inquiry response"""
        
        return {
            "type": "general_response",
            "ai_response": cs_result["response"],
            "intent_detected": cs_result["intent"]["primary_intent"],
            "suggestions": [
                "Ask for restaurant recommendations",
                "Book a table at a specific restaurant",
                "Get information about Chennai's dining scene",
                "Modify or cancel existing bookings"
            ]
        }
    
    def get_system_analytics(self) -> Dict:
        """Get analytics from all agents"""
        
        return {
            "system_performance": {
                "total_interactions": self.system_memory["total_interactions"],
                "successful_bookings": self.system_memory["successful_bookings"],
                "success_rate": (self.system_memory["successful_bookings"] / 
                               max(1, self.system_memory["total_interactions"])) * 100
            },
            "agent_learning_data": {
                "recommendation_agent": {
                    "interactions": len(self.recommendation_agent.memory),
                    "learning_patterns": self.recommendation_agent.learning_data
                },
                "booking_agent": {
                    "interactions": len(self.booking_agent.memory),
                    "active_bookings": len(self.booking_agent.active_bookings)
                },
                "customer_service_agent": {
                    "conversations": len(self.customer_service_agent.conversation_memory),
                    "total_interactions": len(self.customer_service_agent.memory)
                }
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize the agentic system
    agentic_system = AgenticBookingSystem()
    
    # Test various user scenarios
    test_scenarios = [
        "I want to book a table for 4 people tomorrow evening for my anniversary",
        "Can you recommend a good South Indian restaurant in T Nagar?",
        "I need a vegetarian restaurant for a business meeting, budget friendly",
        "Looking for the best seafood place near Marina Beach for 6 people",
        "What's the best restaurant for a birthday celebration with traditional food?"
    ]
    
    print("🤖 Chennai Dining Agentic AI System Demo")
    print("=" * 60)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🎯 Scenario {i}: {scenario}")
        print("-" * 40)
        
        result = agentic_system.process_user_request(scenario)
        
        print(f"🤖 AI Response: {result['ai_response']}")
        
        if result['type'] == 'booking_response':
            if result['booking_success']:
                booking = result['booking_confirmation']
                print(f"✅ Booking Success: {booking['success_message']}")
                print(f"📍 Restaurant: {booking['restaurant']['name']} ({booking['restaurant']['location']})")
            else:
                print(f"❌ Booking Failed: {result['fallback_message']}")
                print(f"🔄 Alternatives: {len(result.get('alternatives', []))} options found")
        
        elif result['type'] == 'recommendation_response':
            print(f"🍽️ Recommendations: {len(result['recommendations'])} restaurants found")
            for rec in result['recommendations'][:2]:  # Show top 2
                print(f"   • {rec['name']} ({rec['location']}) - {rec['rating']}⭐")
    
    # Show system analytics
    print(f"\n📊 System Analytics:")
    analytics = agentic_system.get_system_analytics()
    print(f"   Total Interactions: {analytics['system_performance']['total_interactions']}")
    print(f"   Successful Bookings: {analytics['system_performance']['successful_bookings']}")
    print(f"   Success Rate: {analytics['system_performance']['success_rate']:.1f}%")
    
    print("\n🎉 Agentic AI System Demo Complete!")