from django.core.exceptions import ValidationError


class HabitValidator:
    @staticmethod
    def validate_reward_or_related_habit(data):
        """Проверка: либо вознаграждение, либо связанная привычка"""
        reward = data.get('reward')
        related_habit = data.get('related_habit')

        if reward and related_habit:
            raise ValidationError(
                'Нельзя указать одновременно и вознаграждение, и связанную привычку. '
                'Выберите что-то одно.'
            )

    @staticmethod
    def validate_pleasant_habit(data):
        """Проверка приятной привычки"""
        is_pleasant = data.get('is_pleasant', False)

        if is_pleasant:
            reward = data.get('reward')
            related_habit = data.get('related_habit')

            if reward:
                raise ValidationError('У приятной привычки не может быть вознаграждения.')

            if related_habit:
                raise ValidationError('У приятной привычки не может быть связанной привычки.')

    @staticmethod
    def validate_related_habit_is_pleasant(related_habit):
        """Проверка: связанная привычка должна быть приятной"""
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                'Связанная привычка должна быть приятной привычкой.'
            )

    @staticmethod
    def validate_periodicity(periodicity):
        """Проверка периодичности (не реже 1 раза в 7 дней)"""
        if periodicity > 7:
            raise ValidationError(
                'Привычку нельзя выполнять реже, чем 1 раз в 7 дней.'
            )
        if periodicity < 1:
            raise ValidationError(
                'Периодичность должна быть положительным числом.'
            )

    @staticmethod
    def validate_duration(duration):
        """Проверка времени выполнения (не более 120 секунд)"""
        if duration > 120:
            raise ValidationError(
                'Время выполнения привычки не должно превышать 120 секунд.'
            )
        if duration < 1:
            raise ValidationError(
                'Время выполнения должно быть положительным числом.'
            )