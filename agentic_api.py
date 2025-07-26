#!/usr/bin/env python3
"""
Chennai Dining - Agentic AI API Server
Flask API to connect frontend with multi-agent AI system
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import datetime
from agentic_backend import AgenticBookingSystem
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize the Agentic AI system
agentic_system = AgenticBookingSystem()

@app.route('/')
def index():
    """API Documentation and test interface"""
    api_docs = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chennai Dining - Agentic AI API</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { color: #ff6b35; margin: 0; }
            .header p { color: #666; margin: 10px 0 0 0; }
            .section { margin: 30px 0; }
            .section h2 { color: #333; border-bottom: 2px solid #ff6b35; padding-bottom: 10px; }
            .endpoint { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #ff6b35; }
            .method { display: inline-block; padding: 4px 8px; border-radius: 4px; color: white; font-weight: bold; margin-right: 10px; }
            .method.post { background: #28a745; }
            .method.get { background: #007bff; }
            code { background: #e9ecef; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
            .example { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .test-area { background: #fff3e0; padding: 20px; border-radius: 8px; border: 2px solid #ff6b35; }
            input, textarea, button { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px; font-family: inherit; }
            button { background: #ff6b35; color: white; border: none; cursor: pointer; font-weight: bold; }
            button:hover { background: #e55a2b; }
            .response { background: #f8f9fa; border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin: 10px 0; white-space: pre-wrap; font-family: monospace; }
            .agents { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
            .agent { background: linear-gradient(135deg, #ff6b35, #f7931e); color: white; padding: 20px; border-radius: 10px; }
            .agent h3 { margin: 0 0 10px 0; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
            .feature { background: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Chennai Dining - Agentic AI API</h1>
                <p>Multi-Agent Restaurant Booking System with Autonomous Decision Making</p>
            </div>
            
            <div class="section">
                <h2>🧠 AI Agents Overview</h2>
                <div class="agents">
                    <div class="agent">
                        <h3>🎯 Recommendation Agent</h3>
                        <p>Autonomously analyzes user preferences and recommends perfect restaurants using AI reasoning and learning algorithms.</p>
                    </div>
                    <div class="agent">
                        <h3>📅 Booking Agent</h3>
                        <p>Handles reservation process with intelligent decision making, availability prediction, and autonomous problem solving.</p>
                    </div>
                    <div class="agent">
                        <h3>💬 Customer Service Agent</h3>
                        <p>Processes natural language, understands intent, maintains conversation context, and provides personalized responses.</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🚀 Agentic Features</h2>
                <div class="features">
                    <div class="feature">
                        <h4>🤖 Autonomous Decision Making</h4>
                        <p>AI agents make independent decisions to achieve user goals</p>
                    </div>
                    <div class="feature">
                        <h4>🧠 Machine Learning</h4>
                        <p>Agents learn from interactions and improve over time</p>
                    </div>
                    <div class="feature">
                        <h4>💬 Natural Language</h4>
                        <p>Understands complex user requests in conversational language</p>
                    </div>
                    <div class="feature">
                        <h4>🎯 Goal-Oriented</h4>
                        <p>Each agent pursues specific objectives autonomously</p>
                    </div>
                    <div class="feature">
                        <h4>🔗 Multi-Agent Coordination</h4>
                        <p>Agents work together to solve complex problems</p>
                    </div>
                    <div class="feature">
                        <h4>📊 Transparent Reasoning</h4>
                        <p>AI provides insights into its decision-making process</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📡 API Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method post">POST</span><strong>/api/chat</strong>
                    <p>Main agentic endpoint - send natural language requests to the AI system</p>
                    <div class="example">
                        <strong>Request Body:</strong><br>
                        <code>{"message": "I want to book a table for 4 people tomorrow evening for my anniversary", "user_id": "optional"}</code>
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span><strong>/api/recommend</strong>
                    <p>Get AI-powered restaurant recommendations</p>
                    <div class="example">
                        <strong>Request Body:</strong><br>
                        <code>{"preferences": {"cuisine": "South Indian", "location": "T. Nagar", "group_size": 4}}</code>
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span><strong>/api/book</strong>
                    <p>Book a table using AI booking agent</p>
                    <div class="example">
                        <strong>Request Body:</strong><br>
                        <code>{"restaurant_id": "southern_spice", "user_details": {...}, "preferences": {...}}</code>
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span><strong>/api/analytics</strong>
                    <p>Get system analytics and agent performance data</p>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span><strong>/api/restaurants</strong>
                    <p>Get all available restaurants with AI insights</p>
                </div>
            </div>
            
            <div class="section">
                <h2>🧪 Test the Agentic AI System</h2>
                <div class="test-area">
                    <h3>Try Natural Language Booking:</h3>
                    <textarea id="testMessage" placeholder="Type your request in natural language..." rows="3" style="width: 100%; margin-bottom: 10px;">I want to book a table for 4 people tomorrow evening for my anniversary</textarea><br>
                    <button onclick="testAgenticAPI()">🤖 Send to AI Agents</button>
                    <div id="response" class="response" style="display: none;"></div>
                </div>
            </div>
        </div>
        
        <script>
            async function testAgenticAPI() {
                const message = document.getElementById('testMessage').value;
                const responseDiv = document.getElementById('response');
                
                responseDiv.style.display = 'block';
                responseDiv.textContent = '🤖 AI Agents are processing your request...';
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message})
                    });
                    
                    const result = await response.json();
                    responseDiv.textContent = JSON.stringify(result, null, 2);
                } catch (error) {
                    responseDiv.textContent = 'Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(api_docs)

@app.route('/api/chat', methods=['POST'])
def agentic_chat():
    """
    Main agentic endpoint - processes natural language with multi-agent system
    This is where the AI agents autonomously decide how to handle user requests
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = data.get('user_id', None)
        
        if not user_message:
            return jsonify({
                "error": "Message is required",
                "example": "I want to book a table for 4 people tomorrow evening"
            }), 400
        
        logger.info(f"Agentic AI processing: {user_message}")
        
        # Let the multi-agent system autonomously process the request
        result = agentic_system.process_user_request(user_message, user_id)
        
        # Add timestamp and request info
        result['timestamp'] = datetime.datetime.now().isoformat()
        result['original_request'] = user_message
        result['user_id'] = user_id or result.get('user_id')
        
        logger.info(f"Agentic AI response type: {result.get('type')}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in agentic chat: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "AI agents encountered an error",
            "details": str(e)
        }), 500

@app.route('/api/recommend', methods=['POST'])
def ai_recommendations():
    """
    AI-powered restaurant recommendations using the Recommendation Agent
    """
    try:
        data = request.get_json()
        preferences = data.get('preferences', {})
        
        # Convert preferences to UserPreferences object
        from agentic_backend import UserPreferences
        user_prefs = UserPreferences(
            cuisine_preference=preferences.get('cuisine'),
            location_preference=preferences.get('location'),
            group_size=preferences.get('group_size'),
            occasion=preferences.get('occasion'),
            budget=preferences.get('budget'),
            dietary_restrictions=preferences.get('dietary_restrictions'),
            preferred_time=preferences.get('preferred_time'),
            ambiance_preference=preferences.get('ambiance')
        )
        
        # Get AI recommendations
        recommendations = agentic_system.recommendation_agent.process(user_prefs)
        reasoning = agentic_system.recommendation_agent.get_reasoning_explanation()
        
        result = {
            "type": "ai_recommendations",
            "recommendations": [
                {
                    "id": r.id,
                    "name": r.name,
                    "location": r.location,
                    "cuisine": r.cuisine_type,
                    "rating": r.rating,
                    "price_range": r.price_range,
                    "specialties": r.specialties,
                    "features": r.features,
                    "capacity": r.capacity,
                    "available_times": r.available_times
                } for r in recommendations
            ],
            "ai_reasoning": reasoning,
            "preferences_analyzed": preferences,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in AI recommendations: {str(e)}")
        return jsonify({
            "error": "Recommendation error",
            "message": "AI recommendation agent encountered an error",
            "details": str(e)
        }), 500

@app.route('/api/book', methods=['POST'])
def ai_booking():
    """
    AI-powered booking using the Booking Agent
    """
    try:
        data = request.get_json()
        restaurant_id = data.get('restaurant_id')
        user_details = data.get('user_details', {})
        preferences = data.get('preferences', {})
        
        if not restaurant_id:
            return jsonify({
                "error": "Restaurant ID is required",
                "available_restaurants": [
                    "southern_spice", "chettinad_palace", "coastal_kitchen",
                    "mylapore_mess", "namma_veedu", "royal_feast"
                ]
            }), 400
        
        # Find the restaurant
        restaurant = None
        for r in agentic_system.recommendation_agent.restaurants_db:
            if r.id == restaurant_id:
                restaurant = r
                break
        
        if not restaurant:
            return jsonify({
                "error": "Restaurant not found",
                "restaurant_id": restaurant_id
            }), 404
        
        # Create booking request
        from agentic_backend import BookingRequest, UserPreferences
        user_prefs = UserPreferences(
            cuisine_preference=preferences.get('cuisine'),
            location_preference=preferences.get('location'),
            group_size=preferences.get('group_size'),
            occasion=preferences.get('occasion'),
            budget=preferences.get('budget'),
            dietary_restrictions=preferences.get('dietary_restrictions'),
            preferred_time=preferences.get('preferred_time')
        )
        
        booking_request = BookingRequest(
            user_id=user_details.get('user_id', f"user_{datetime.datetime.now().timestamp()}"),
            message=f"Book table at {restaurant.name}",
            preferences=user_prefs,
            timestamp=datetime.datetime.now()
        )
        
        # Let AI booking agent handle the reservation
        booking_result = agentic_system.booking_agent.process(booking_request, [restaurant])
        
        result = {
            "type": "ai_booking",
            "success": booking_result.success,
            "booking_id": booking_result.booking_id,
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name,
                "location": restaurant.location,
                "rating": restaurant.rating
            } if restaurant else None,
            "confirmation_details": booking_result.confirmation_details,
            "ai_reasoning": booking_result.agent_reasoning,
            "alternatives": [
                {
                    "id": r.id,
                    "name": r.name,
                    "location": r.location,
                    "rating": r.rating
                } for r in booking_result.alternative_suggestions
            ],
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in AI booking: {str(e)}")
        return jsonify({
            "error": "Booking error",
            "message": "AI booking agent encountered an error",
            "details": str(e)
        }), 500

@app.route('/api/analytics', methods=['GET'])
def system_analytics():
    """
    Get analytics and performance data from all AI agents
    """
    try:
        analytics = agentic_system.get_system_analytics()
        
        # Add current system status
        analytics['system_status'] = {
            "active_agents": 3,
            "agents_info": {
                "recommendation_agent": {
                    "name": agentic_system.recommendation_agent.name,
                    "goal": agentic_system.recommendation_agent.goal,
                    "restaurant_database_size": len(agentic_system.recommendation_agent.restaurants_db)
                },
                "booking_agent": {
                    "name": agentic_system.booking_agent.name,
                    "goal": agentic_system.booking_agent.goal,
                    "active_bookings": len(agentic_system.booking_agent.active_bookings)
                },
                "customer_service_agent": {
                    "name": agentic_system.customer_service_agent.name,
                    "goal": agentic_system.customer_service_agent.goal,
                    "active_conversations": len(agentic_system.customer_service_agent.conversation_memory)
                }
            }
        }
        
        analytics['timestamp'] = datetime.datetime.now().isoformat()
        
        return jsonify(analytics)
        
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        return jsonify({
            "error": "Analytics error",
            "details": str(e)
        }), 500

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    """
    Get all restaurants with AI insights and recommendations
    """
    try:
        restaurants = agentic_system.recommendation_agent.restaurants_db
        
        result = {
            "type": "restaurant_database",
            "total_restaurants": len(restaurants),
            "restaurants": [
                {
                    "id": r.id,
                    "name": r.name,
                    "location": r.location,
                    "cuisine_type": r.cuisine_type,
                    "rating": r.rating,
                    "price_range": r.price_range,
                    "specialties": r.specialties,
                    "capacity": r.capacity,
                    "available_times": r.available_times,
                    "features": r.features,
                    "reviews_count": r.reviews_count,
                    "ai_insights": {
                        "popularity_score": r.rating * r.reviews_count / 100,
                        "capacity_category": "intimate" if r.capacity < 60 else "spacious" if r.capacity > 100 else "medium",
                        "price_category": "budget" if "low" in r.price_range else "premium" if "high" in r.price_range else "moderate"
                    }
                } for r in restaurants
            ],
            "ai_metadata": {
                "cuisine_types": list(set(r.cuisine_type for r in restaurants)),
                "locations": list(set(r.location for r in restaurants)),
                "price_ranges": list(set(r.price_range for r in restaurants)),
                "total_capacity": sum(r.capacity for r in restaurants),
                "average_rating": sum(r.rating for r in restaurants) / len(restaurants)
            },
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting restaurants: {str(e)}")
        return jsonify({
            "error": "Database error",
            "details": str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test_agentic_system():
    """
    Test endpoint to verify the agentic system is working
    """
    try:
        # Test all agents with a sample request
        test_message = "Can you recommend a good South Indian restaurant for 4 people?"
        result = agentic_system.process_user_request(test_message, "test_user")
        
        return jsonify({
            "status": "success",
            "message": "Agentic AI system is working correctly",
            "test_request": test_message,
            "test_response": result,
            "system_health": {
                "recommendation_agent": "active",
                "booking_agent": "active", 
                "customer_service_agent": "active"
            },
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in system test: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Agentic system test failed",
            "error": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/api/chat",
            "/api/recommend", 
            "/api/book",
            "/api/analytics",
            "/api/restaurants",
            "/api/test"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "AI agents encountered an unexpected error"
    }), 500

if __name__ == '__main__':
    print("🤖 Starting Chennai Dining Agentic AI API Server...")
    print("=" * 60)
    print("🧠 Initializing AI Agents:")
    print(f"   • {agentic_system.recommendation_agent.name}")
    print(f"   • {agentic_system.booking_agent.name}")
    print(f"   • {agentic_system.customer_service_agent.name}")
    print("=" * 60)
    print("🌐 API Server running at: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000")
    print("🧪 Test Endpoint: http://localhost:5000/api/test")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)