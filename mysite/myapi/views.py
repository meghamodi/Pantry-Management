from django.shortcuts import render
from django.http import HttpResponse
from .app import main
from django.http import HttpResponse, JsonResponse
from .scraping import scan_and_insert
from django.views.decorators.csrf import csrf_exempt
import json


# def barcode_scan(request):
#     # Render the barcode scanner HTML page
#     return render(request, 'barcode_scan.html')

@csrf_exempt 
def barcode_scan_only(request):
    """Just scan barcode without web scraping - useful for testing"""
    try:
        print("📷 Starting barcode scan only...")
        barcode = main()
        
        if barcode:
            return JsonResponse({
                'success': True, 
                'barcode': barcode,
                'message': f'Barcode scanned successfully: {barcode}'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No barcode detected'
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error during barcode scan: {str(e)}'
        }, status=500)
    
@csrf_exempt
def scan_and_insert_view(request):
    # Get the product ID from the barcode scanner
    """Handle barcode scanning and product insertion"""
    try:
        print("🎯 Starting scan_and_insert_view...")
        
        # Call the scanning and insertion function
        result = scan_and_insert()
        
        if result is None:
            return HttpResponse("⚠️ No barcode detected or scanning failed.", status=400)
        
        # Unpack the result
        if isinstance(result, tuple) and len(result) == 2:
            product_id, product_info = result
            
            if product_id:
                response_message = f"✅ Product found!\nBarcode: {product_id}\nProduct: {product_info}"
                print(f"✅ Success: {response_message}")
                return HttpResponse(response_message)
            else:
                return HttpResponse(f"❌ Error: {product_info}", status=400)
        else:
            return HttpResponse("❌ Unexpected result format from scanner.", status=500)
            
    except Exception as e:
        error_message = f"❌ Error in scan_and_insert_view: {str(e)}"
        print(error_message)
        return HttpResponse(error_message, status=500)



