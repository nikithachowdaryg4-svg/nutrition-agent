class HealthAdvisoryAgent:

    def get_advice(self, health_condition):

        condition = health_condition.lower()

        # ---------------- DIABETES ----------------
        if "diabetes" in condition:

            return {
                "Condition": "🩸 Diabetes",
                "Advice": [
                    "Choose high-fiber foods such as vegetables, legumes and whole grains.",
                    "Limit sugary drinks, sweets and foods with added sugar.",
                    "Control carbohydrate portions and choose whole grains.",
                    "Choose whole fruits instead of fruit juices.",
                    "Include balanced meals with protein and vegetables."
                ]
            }

        # ---------------- HEART DISEASE ----------------
        elif "heart" in condition:

            return {
                "Condition": "❤️ Heart Disease",
                "Advice": [
                    "Include vegetables, fruits and whole grains regularly.",
                    "Choose healthier unsaturated fats from nuts, seeds and fish.",
                    "Limit foods high in saturated and trans fats.",
                    "Reduce excessive salt and highly processed foods.",
                    "Choose lean protein sources such as fish, legumes and tofu."
                ]
            }

        # ---------------- HYPERTENSION ----------------
        elif "hypertension" in condition or "high blood pressure" in condition:

            return {
                "Condition": "🩺 Hypertension",
                "Advice": [
                    "Reduce excessive salt and high-sodium foods.",
                    "Include vegetables and fruits regularly.",
                    "Prefer fresh foods instead of highly processed foods.",
                    "Choose whole grains and fiber-rich foods.",
                    "Maintain balanced meals and healthy portion sizes."
                ]
            }

        # ---------------- HIGH CHOLESTEROL ----------------
        elif "cholesterol" in condition:

            return {
                "Condition": "🫀 High Cholesterol",
                "Advice": [
                    "Include fiber-rich foods such as oats, vegetables and legumes.",
                    "Choose nuts, seeds and other sources of unsaturated fats.",
                    "Limit foods high in saturated and trans fats.",
                    "Choose lean protein and fish more often.",
                    "Reduce fried and highly processed foods."
                ]
            }

        # ---------------- ANEMIA ----------------
        elif "anemia" in condition or "anaemia" in condition:

            return {
                "Condition": "🩸 Anemia",
                "Advice": [
                    "Include iron-rich foods such as legumes, spinach and lean meats.",
                    "Combine plant-based iron sources with vitamin-C-rich foods.",
                    "Include a variety of protein-rich foods.",
                    "Eat a balanced diet containing vegetables and fruits.",
                    "For diagnosed anemia, follow advice from a healthcare professional."
                ]
            }

        # ---------------- PCOS ----------------
        elif "pcos" in condition:

            return {
                "Condition": "🌸 PCOS",
                "Advice": [
                    "Include vegetables, whole grains and fiber-rich foods.",
                    "Choose protein-rich foods such as eggs, fish, tofu and legumes.",
                    "Limit excessive added sugar and highly processed foods.",
                    "Prefer balanced meals instead of frequent sugary snacks.",
                    "Include healthy fats such as nuts, seeds and avocado."
                ]
            }

        # ---------------- THYROID ----------------
        elif "thyroid" in condition:

            return {
                "Condition": "🦋 Thyroid Disorder",
                "Advice": [
                    "Maintain a balanced diet with adequate protein.",
                    "Include a variety of vegetables, fruits and whole grains.",
                    "Include nutrient-rich foods containing iodine, selenium and zinc.",
                    "Avoid taking high-dose supplements without professional advice.",
                    "Follow the dietary and medication guidance provided by your doctor."
                ]
            }

        # ---------------- OSTEOPOROSIS ----------------
        elif "osteoporosis" in condition:

            return {
                "Condition": "🦴 Osteoporosis",
                "Advice": [
                    "Include calcium-rich foods such as milk, curd and fortified foods.",
                    "Include adequate protein in the diet.",
                    "Include vitamin-D-rich foods and appropriate sunlight exposure.",
                    "Choose vegetables and fruits as part of a balanced diet.",
                    "Follow professional advice regarding calcium and vitamin D supplements."
                ]
            }

        # ---------------- OBESITY ----------------
        elif "obesity" in condition:

            return {
                "Condition": "⚖️ Obesity",
                "Advice": [
                    "Focus on vegetables, fruits, whole grains and protein-rich foods.",
                    "Control portion sizes.",
                    "Limit sugary drinks and highly processed foods.",
                    "Choose nutrient-dense foods instead of calorie-dense snacks.",
                    "Combine healthy eating with regular physical activity."
                ]
            }

        # ---------------- KIDNEY DISEASE ----------------
        elif "kidney" in condition:

            return {
                "Condition": "🫁 Kidney Disease",
                "Advice": [
                    "Follow the individualized diet plan recommended by a healthcare professional.",
                    "Monitor sodium intake and avoid excessive processed foods.",
                    "Protein, potassium and phosphorus requirements may vary by condition.",
                    "Stay hydrated according to medical advice.",
                    "Do not make major dietary changes without professional guidance."
                ]
            }

        # ---------------- ASTHMA ----------------
        elif "asthma" in condition:

            return {
                "Condition": "🫁 Asthma",
                "Advice": [
                    "Maintain a balanced diet rich in vegetables and fruits.",
                    "Include adequate protein and whole grains.",
                    "Choose healthy sources of fats such as nuts and seeds.",
                    "Maintain a healthy body weight.",
                    "Avoid foods that personally trigger symptoms or allergies."
                ]
            }

        # ---------------- MIGRAINE ----------------
        elif "migraine" in condition:

            return {
                "Condition": "🧠 Migraine",
                "Advice": [
                    "Maintain regular meal timings.",
                    "Stay adequately hydrated.",
                    "Avoid skipping meals.",
                    "Identify and avoid personal food triggers.",
                    "Limit excessive caffeine if it triggers symptoms."
                ]
            }

        # ---------------- ARTHRITIS ----------------
        elif "arthritis" in condition:

            return {
                "Condition": "🦴 Arthritis",
                "Advice": [
                    "Include vegetables and fruits regularly.",
                    "Choose healthy fats such as those found in fish, nuts and seeds.",
                    "Include adequate protein for overall nutrition.",
                    "Maintain a healthy body weight.",
                    "Limit highly processed foods and excessive added sugar."
                ]
            }

        # ---------------- LACTOSE INTOLERANCE ----------------
        elif "lactose" in condition:

            return {
                "Condition": "🥛 Lactose Intolerance",
                "Advice": [
                    "Identify and limit foods that cause lactose-related symptoms.",
                    "Consider lactose-free milk or suitable alternatives.",
                    "Include calcium-rich non-dairy foods when needed.",
                    "Check food labels for hidden sources of lactose.",
                    "Discuss persistent symptoms with a healthcare professional."
                ]
            }

        # ---------------- CELIAC DISEASE ----------------
        elif "celiac" in condition:

            return {
                "Condition": "🌾 Celiac Disease",
                "Advice": [
                    "Follow a strict gluten-free diet as medically advised.",
                    "Choose naturally gluten-free foods such as rice, fruits and vegetables.",
                    "Check food labels carefully for gluten-containing ingredients.",
                    "Avoid cross-contamination with gluten-containing foods.",
                    "Consult a dietitian for a nutritionally balanced gluten-free diet."
                ]
            }

        # ---------------- FATTY LIVER ----------------
        elif "fatty liver" in condition:

            return {
                "Condition": "🫃 Fatty Liver Disease",
                "Advice": [
                    "Choose vegetables, fruits, whole grains and lean protein.",
                    "Limit foods high in added sugar.",
                    "Avoid excessive intake of highly processed and fried foods.",
                    "Choose healthier unsaturated fats.",
                    "Maintain a healthy body weight through balanced nutrition and activity."
                ]
            }

        # ---------------- VITAMIN D DEFICIENCY ----------------
        elif "vitamin d" in condition:

            return {
                "Condition": "🧪 Vitamin D Deficiency",
                "Advice": [
                    "Include vitamin-D-rich or fortified foods.",
                    "Include calcium-rich foods such as milk and curd.",
                    "Appropriate sunlight exposure may help vitamin D production.",
                    "Maintain a balanced diet with adequate protein.",
                    "Take vitamin D supplements only according to professional advice."
                ]
            }

        # ---------------- VITAMIN B12 DEFICIENCY ----------------
        elif "vitamin b12" in condition or "b12" in condition:

            return {
                "Condition": "🧪 Vitamin B12 Deficiency",
                "Advice": [
                    "Include B12-containing foods such as eggs, dairy and animal-based foods.",
                    "Vegetarians and vegans may need fortified foods or supplements.",
                    "Maintain a varied and balanced diet.",
                    "Discuss persistent deficiency with a healthcare professional.",
                    "Take B12 supplements according to professional advice."
                ]
            }

        # ---------------- GENERAL ----------------
        elif "healthy" in condition:

            return {
                "Condition": "🥗 General Healthy Nutrition",
                "Advice": [
                    "Eat a variety of vegetables and fruits.",
                    "Include adequate protein in meals.",
                    "Prefer whole grains and high-fiber foods.",
                    "Stay hydrated throughout the day.",
                    "Limit excessive sugar, salt and highly processed foods."
                ]
            }

        # ---------------- DEFAULT ----------------
        else:

            return {
                "Condition": "🌱 General Nutrition Guidance",
                "Advice": [
                    "Maintain a balanced diet containing vegetables, fruits, protein and whole grains.",
                    "Stay hydrated throughout the day.",
                    "Choose minimally processed foods whenever possible.",
                    "Maintain appropriate portion sizes.",
                    "Consult a qualified healthcare professional for specific medical conditions."
                ]
            }