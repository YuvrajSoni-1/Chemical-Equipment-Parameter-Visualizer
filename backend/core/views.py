from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DatasetWrapper, EquipmentData
from .serializers import DatasetWrapperSerializer, EquipmentDataSerializer
import pandas as pd
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class UploadView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # Enforce 5 dataset limit
        datasets = DatasetWrapper.objects.all().order_by('upload_date')
        if datasets.count() >= 5:
            # Delete oldest
            datasets.first().delete()

        try:
            # Parse CSV
            df = pd.read_csv(file)
            # Basic validation
            required_cols = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            if not all(col in df.columns for col in required_cols):
                 return Response({'error': f'Missing columns. Required: {required_cols}'}, status=status.HTTP_400_BAD_REQUEST)

            # Create Dataset Object
            dataset = DatasetWrapper.objects.create(filename=file.name)

            # Create Equipment Objects
            equipment_list = []
            for _, row in df.iterrows():
                equipment_list.append(EquipmentData(
                    dataset=dataset,
                    equipment_name=row['Equipment Name'],
                    equipment_type=row['Type'],
                    flowrate=row['Flowrate'],
                    pressure=row['Pressure'],
                    temperature=row['Temperature']
                ))
            
            EquipmentData.objects.bulk_create(equipment_list)
            
            return Response({'message': 'File uploaded successfully', 'id': dataset.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistoryView(APIView):
    def get(self, request):
        datasets = DatasetWrapper.objects.all().order_by('-upload_date')
        serializer = DatasetWrapperSerializer(datasets, many=True)
        return Response(serializer.data)

class AnalysisView(APIView):
    def get(self, request, id):
        try:
            dataset = DatasetWrapper.objects.get(id=id)
        except DatasetWrapper.DoesNotExist:
             return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = EquipmentData.objects.filter(dataset=dataset)
        
        total_count = data.count()
        if total_count == 0:
             return Response({'message': 'No data'}, status=status.HTTP_200_OK)
             
        # Manual aggregations or pandas
        # Let's use Django ORM aggregation for simplicity or pandas if we wanna be fancy. Pandas is already required.
        # Let's use pandas since we might load it anyway for complex stuff, but here ORM is faster.
        # Actually requirements say "Data Analysis API"
        
        from django.db.models import Avg, Count
        stats = data.aggregate(
            avg_flowrate=Avg('flowrate'),
            avg_pressure=Avg('pressure'),
            avg_temperature=Avg('temperature')
        )
        
        type_distribution = data.values('equipment_type').annotate(count=Count('equipment_type'))
        
        # Raw data for charts
        raw_serializer = EquipmentDataSerializer(data, many=True)

        return Response({
            'stats': {
                'total_count': total_count,
                 **stats
            },
            'type_distribution': type_distribution,
            'raw_data': raw_serializer.data # Sending raw data for frontend charts
        })

class ReportView(APIView):
    def get(self, request, id):
        try:
            dataset = DatasetWrapper.objects.get(id=id)
        except DatasetWrapper.DoesNotExist:
             return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, height - 50, f"Report for {dataset.filename}")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 80, f"Uploaded on: {dataset.upload_date}")

        data = EquipmentData.objects.filter(dataset=dataset)
        from django.db.models import Avg
        stats = data.aggregate(Avg('flowrate'), Avg('pressure'), Avg('temperature'))
        
        p.drawString(50, height - 120, f"Total Equipment: {data.count()}")
        
        avg_flow = stats['flowrate__avg'] if stats['flowrate__avg'] is not None else 0.0
        avg_press = stats['pressure__avg'] if stats['pressure__avg'] is not None else 0.0
        avg_temp = stats['temperature__avg'] if stats['temperature__avg'] is not None else 0.0
        
        p.drawString(50, height - 140, f"Avg Flowrate: {avg_flow:.2f}")
        p.drawString(50, height - 160, f"Avg Pressure: {avg_press:.2f}")
        p.drawString(50, height - 180, f"Avg Temperature: {avg_temp:.2f}")

        # Simple list loop
        y = height - 220
        p.drawString(50, y, "Equipment List (First 20 items):")
        y -= 20
        for item in data[:20]:
            if y < 50: break
            p.drawString(50, y, f"{item.equipment_name} - {item.equipment_type}: T={item.temperature} P={item.pressure} F={item.flowrate}")
            y -= 15

        p.showPage()
        p.save()
        

class APIRootView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Chemical Equipment Visualizer API',
            'endpoints': {
                'upload': '/api/upload/',
                'history': '/api/history/',
                'analysis': '/api/analysis/<id>/',
                'report': '/api/report/<id>/'
            }
        })

