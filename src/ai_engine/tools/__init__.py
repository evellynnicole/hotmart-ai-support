from src.ai_engine.tools.customer_service import customer_service
from src.ai_engine.tools.get_billing_info import get_billing_info
from src.ai_engine.tools.retriever import retrieve_faq

tools_faq = [
    retrieve_faq,
    customer_service,
]

tools_journey = [
    get_billing_info,
    customer_service,
]
