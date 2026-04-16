from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DispatchPlanSerializer, GeneratePlanSerializer
from .services import DecisionPlanService


class DecisionPlansView(APIView):
    service_class = DecisionPlanService

    def get(self, request):
        service = self.service_class()
        selected_block = request.GET.get("block_code") or None
        return Response({"code": 0, "message": "ok", "data": service.build_plans_payload(selected_block=selected_block)})


class DecisionGenerateView(APIView):
    service_class = DecisionPlanService

    def post(self, request):
        serializer = GeneratePlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        block_code = serializer.validated_data["block_code"]
        service = self.service_class()
        generated = service.generate_plan(block_code)

        return Response(
            {
                "code": 0,
                "message": "新策略已生成",
                "data": {
                    "generated_plan": generated,
                    "plans_payload": service.build_plans_payload(selected_block=block_code),
                },
            }
        )


class DecisionDispatchView(APIView):
    service_class = DecisionPlanService

    def post(self, request):
        serializer = DispatchPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_code = serializer.validated_data["plan_code"]
        service = self.service_class()
        dispatch_preview = service.dispatch_plan(plan_code)
        if dispatch_preview is None:
            return Response({"code": 1, "message": "未找到对应策略", "data": {}}, status=404)

        return Response(
            {
                "code": 0,
                "message": "策略已进入下发预留状态",
                "data": {
                    "dispatch": dispatch_preview,
                    "plans_payload": service.build_plans_payload(),
                },
            }
        )
