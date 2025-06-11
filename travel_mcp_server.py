import gradio as gr
from typing import Dict, List, Any

class TravelDocumentationService:
    """Service for fetching travel documentation requirements"""
        
    def get_visa_requirements(
        self, 
        from_country: str, 
        to_country: str, 
        trip_duration: int = 30
    ) -> Dict[str, Any]:
        """Get visa requirements for travel between countries"""
        
        # Mock data
        visa_free_combinations = {
            ("canada", "japan"): {"visa_required": False, "max_stay": "90 days"},
            ("canada", "uk"): {"visa_required": False, "max_stay": "6 months"},
            ("canada", "usa"): {"visa_required": False, "max_stay": "6 months"},
            ("canada", "germany"): {"visa_required": False, "max_stay": "90 days"},
            ("usa", "japan"): {"visa_required": False, "max_stay": "90 days"},
            ("usa", "uk"): {"visa_required": False, "max_stay": "6 months"},
            ("usa", "germany"): {"visa_required": False, "max_stay": "90 days"},
            ("china", "japan"): {"visa_required": True, "visa_type": "Tourist Visa", "max_stay": "30 days", "processing_time": "5-7 business days", "fee": "$30 USD"},
            ("india", "japan"): {"visa_required": True, "visa_type": "Tourist Visa", "max_stay": "90 days", "processing_time": "5-10 business days", "fee": "$50 USD"},
            ("china", "usa"): {"visa_required": True, "visa_type": "B-2 Tourist Visa", "max_stay": "6 months", "processing_time": "3-5 weeks", "fee": "$160 USD"},
            ("india", "usa"): {"visa_required": True, "visa_type": "B-2 Tourist Visa", "max_stay": "6 months", "processing_time": "3-5 weeks", "fee": "$160 USD"},
        }
        
        key = (from_country.lower(), to_country.lower())
        
        if key in visa_free_combinations:
            return visa_free_combinations[key]
        else:
            return {
                "visa_required": True,
                "visa_type": "Tourist Visa",
                "max_stay": "30 days",
                "processing_time": "5-10 business days",
                "fee": "$50-150 USD"
            }
    
    def get_document_requirements(
        self,
        from_country: str,
        to_country: str,
        trip_duration: int = 30,
        trip_purpose: str = "tourism"
    ) -> List[Dict[str, Any]]:
        """Get comprehensive document requirements for travel"""
        
        requirements = []
        
        requirements.append({
            "document_type": "Passport",
            "required": True,
            "description": "Valid passport with at least 6 months validity remaining",
            "validity_period": "At least 6 months from travel date",
            "additional_notes": "Must have at least 2 blank pages for stamps"
        })
        
        visa_info = self.get_visa_requirements(from_country, to_country, trip_duration)
        
        if visa_info.get("visa_required", False):
            requirements.append({
                "document_type": "Visa",
                "required": True,
                "description": f"Required {visa_info.get('visa_type', 'Tourist Visa')}",
                "processing_time": visa_info.get("processing_time", "5-10 business days"),
                "additional_notes": f"Fee: {visa_info.get('fee', 'Varies by embassy')}"
            })
        
        insurance_required_countries = ["schengen", "germany", "france", "italy", "spain", "netherlands", "austria", "belgium"]
        if to_country.lower() in insurance_required_countries:
            requirements.append({
                "document_type": "Travel Insurance",
                "required": True,
                "description": "Travel insurance with minimum €30,000 coverage",
                "additional_notes": "Required for Schengen area countries"
            })
        else:
            requirements.append({
                "document_type": "Travel Insurance",
                "required": False,
                "description": "Travel insurance (highly recommended)",
                "additional_notes": "Covers medical emergencies, trip cancellation, etc."
            })
        
        requirements.append({
            "document_type": "Return/Onward Ticket",
            "required": True,
            "description": "Proof of return or onward travel",
            "additional_notes": "Flight confirmation or travel itinerary"
        })
        
        financial_amount = "$100-150 per day" if to_country.lower() in ["japan", "switzerland", "norway"] else "$50-100 per day"
        requirements.append({
            "document_type": "Financial Proof",
            "required": True,
            "description": f"Proof of sufficient funds ({financial_amount})",
            "additional_notes": "Bank statements, credit cards, or traveler's checks"
        })
        
        requirements.append({
            "document_type": "Accommodation Proof",
            "required": True,
            "description": "Hotel booking or invitation letter",
            "additional_notes": "Confirmation of where you'll be staying"
        })
        
        if trip_purpose.lower() == "business":
            requirements.append({
                "document_type": "Business Invitation Letter",
                "required": True,
                "description": "Letter from host company",
                "additional_notes": "Must include company details and purpose of visit"
            })
        elif trip_purpose.lower() == "study":
            requirements.append({
                "document_type": "Student Visa/Permit",
                "required": True,
                "description": "Student visa or study permit",
                "additional_notes": "Issued by educational institution"
            })
            requirements.append({
                "document_type": "Acceptance Letter",
                "required": True,
                "description": "Letter of acceptance from educational institution",
                "additional_notes": "Must be from recognized institution"
            })
        
        return requirements

travel_service = TravelDocumentationService()

def get_requirements(from_country, to_country, trip_duration, trip_purpose):
    """
    Analyze the documentation requirment for user's travel plan

    Args:
        from_country (str): User's original country
        to_country (str): The destination country that the user plans to travel to
        trip_duration (number): The days length that the user plans to stay in the destination country
        trip_purpose (str): The purpose of the travel, the user is go for business, tourism, study or other purposes

    Returns:
        json: Contains the comprehensive documentation requires and suggestions based on the user input
    """
    try:
        requirements = travel_service.get_document_requirements(
            from_country, to_country, int(trip_duration), trip_purpose
        )
        
        visa_info = travel_service.get_visa_requirements(from_country, to_country, int(trip_duration))
        
        required_docs = [req for req in requirements if req['required']]
        optional_docs = [req for req in requirements if not req['required']]
        
        result = {
            "trip_info": {
                "from_country": from_country.title(),
                "to_country": to_country.title(),
                "duration_days": int(trip_duration),
                "purpose": trip_purpose.title()
            },
            "visa_requirements": {
                "visa_required": visa_info.get("visa_required", False),
                "visa_type": visa_info.get("visa_type"),
                "max_stay": visa_info.get("max_stay"),
                "processing_time": visa_info.get("processing_time"),
                "fee": visa_info.get("fee")
            },
            "required_documents": required_docs,
            "optional_documents": optional_docs,
            "total_documents": len(requirements),
            "summary": {
                "required_count": len(required_docs),
                "optional_count": len(optional_docs),
                "visa_needed": visa_info.get("visa_required", False)
            }
        }
        
        return result
        
    except Exception as e:
        return {"error": str(e)}


travel_demo = gr.Interface(
    fn=get_requirements,
    inputs=[
        gr.Textbox(label="Your Citizenship Country", placeholder="e.g., Canada", value="Canada"),
        gr.Textbox(label="Destination Country", placeholder="e.g., Japan", value="Japan"),
        gr.Number(label="Trip Duration (days)", value=30, minimum=1, maximum=365),
        gr.Dropdown(label="Trip Purpose", choices=["tourism", "business", "transit", "study", "work", "family visit"], value="tourism")
    ],
    outputs=gr.JSON(),
    title="Travel Documentation Requirements",
    description="Get the comprehensive travel documentation requirements for international travel"
)

if __name__ == "__main__":
    travel_demo.launch(
        # share=True,
        show_error=True,
        mcp_server=True,
        # server_port=7861
    )
