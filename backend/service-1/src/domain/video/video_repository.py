"""service-1: Video Repository Interface (Abstract)."""

from abc import ABC, abstractmethod

from src.domain.video.video import Video


class VideoRepository(ABC):
    """Video 애그리게이트 영속성 계약.

    Infrastructure 계층이 이 인터페이스를 구현한다.
    Domain/Application 계층은 이 추상 타입에만 의존한다.
    """

    @abstractmethod
    def get_by_id(self, video_id: int) -> Video | None:
        ...

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100) -> list[Video]:
        ...

    @abstractmethod
    def save(self, video: Video) -> Video:
        """생성 또는 업데이트."""
        ...

    @abstractmethod
    def delete(self, video_id: int) -> bool:
        ...
