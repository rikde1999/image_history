from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from image_app.models import User, Interaction, Image
from image_app.serializers import InteractionSerializer, OTPVerificationSerializer


class RegisterView(APIView):
    def post(self, request):
        mobile_number = request.data.get("mobile_number")
        if not mobile_number:
            return Response(
                {"error": "Mobile number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate and send OTP (dummy OTP for simplicity)
        otp = "123456"
        user, created = User.objects.get_or_create(mobile_number=mobile_number)
        user.otp = otp
        user.save()

        return Response(
            {"success": True, "message": "OTP sent successfully."},
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data.get("mobile_number")
            otp = serializer.validated_data.get("otp")
            name = serializer.validated_data.get("name")

            try:
                user = User.objects.get(mobile_number=mobile_number, otp=otp)
                user.is_verified = True
                if name:
                    user.name = name
                user.save()

                return Response(
                    {
                        "success": True,
                        "message": "Verification successful.",
                        "user_id": user.id,
                    },
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid OTP or mobile number"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomepageView(APIView):
    def get(self, request):
        images = Image.objects.all()
        image_data = [{"url": image.url, "name": image.name} for image in images]
        return Response({"images": image_data}, status=status.HTTP_200_OK)


class ImageInteractionView(APIView):
    def post(self, request):

        serializer = InteractionSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get("user_id")
            image_name = serializer.validated_data.get("image_name")
            action = serializer.validated_data.get("action")

            try:
                user = User.objects.get(id=user_id, is_verified=True)
                Interaction.objects.create(
                    user=user, image_name=image_name, action=action
                )
                message = f"{user.name}, you have {action} image {image_name}"
                return Response(
                    {"success": True, "message": message}, status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HistoryView(APIView):
    def get(self, request):
        user_id = request.query_params.get(
            "user_id"
        )  # Get the user_id from query parameters

        if not user_id:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
            interactions = Interaction.objects.filter(user=user).order_by("-timestamp")
            serializer = InteractionSerializer(interactions, many=True)
            return Response({"history": serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST
            )


"""
class CompletionView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            return Response({'message': f'{user.name}, you have rated all the images. Thank You!'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
"""
