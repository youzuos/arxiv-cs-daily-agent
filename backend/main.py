from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from agents.code_evaluation_agent import CodeEvaluationAgent
from agents.code_generation_agent import CodeGenerationAgent
from agents.planning_agent import PlanningAgent
from orchestrator.orchestrator import MultiAgentOrchestrator
from tools.command_executor import CommandExecutor
from tools.file_manager import FileManager
from tools.llm_client import LLMClient

# 配置日志文件
BASE_DIR = Path(__file__).resolve().parents[1]
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / f"agent_{datetime.now().strftime('%Y%m%d')}.log"

# 移除默认handler，添加文件和控制台输出
logger.remove()
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    encoding="utf-8",
)
logger.add(
    lambda msg: print(msg, end=""),
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
)

# 初始化工具和智能体
file_manager = FileManager()
command_executor = CommandExecutor()
llm_client = LLMClient()
planner = PlanningAgent(name="planner")
coder = CodeGenerationAgent(name="coder", tools=[file_manager, command_executor, llm_client])
evaluator = CodeEvaluationAgent(name="evaluator", tools=[command_executor])
orchestrator = MultiAgentOrchestrator(planner, coder, evaluator)

PAPERS_FILE = BASE_DIR / "frontend" / "src" / "data" / "papers.json"

# 全局调度器
scheduler = BackgroundScheduler()


def daily_update_job():
    """每日更新任务：使用多智能体系统更新论文数据"""
    logger.info("🔄 Starting daily update job...")
    try:
        orchestrator.bootstrap("daily refresh")
        orchestrator.run()
        logger.info("✅ Daily update completed successfully")
    except Exception as e:
        logger.error(f"❌ Daily update failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：启动和关闭调度器"""
    # 启动时：设置每日更新任务（每天凌晨2点执行）
    scheduler.add_job(
        daily_update_job,
        trigger=CronTrigger(hour=2, minute=0),  # 每天凌晨2点
        id="daily_update",
        name="Daily Paper Update",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("📅 Daily update scheduler started (runs daily at 02:00)")
    yield
    # 关闭时：停止调度器
    scheduler.shutdown()
    logger.info("📅 Daily update scheduler stopped")


app = FastAPI(title="arXiv CS Daily Agent", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/run")
def run_project(requirement: str):
    """手动触发多智能体任务"""
    orchestrator.bootstrap(requirement)
    orchestrator.run()
    return {"tasks": orchestrator.summary()}


@app.post("/update")
def trigger_daily_update():
    """手动触发每日更新（不等待定时任务）"""
    logger.info("🔄 Manual daily update triggered")
    try:
        orchestrator.bootstrap("daily refresh")
        orchestrator.run()
        return {
            "status": "success",
            "message": "Daily update completed",
            "tasks": orchestrator.summary()
        }
    except Exception as e:
        logger.error(f"❌ Manual update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/papers")
def list_papers():
    """获取论文列表"""
    if not PAPERS_FILE.exists():
        raise HTTPException(status_code=404, detail="papers.json not generated yet")
    import json
    data = json.loads(PAPERS_FILE.read_text(encoding="utf-8"))
    return {"papers": data}


@app.get("/scheduler/status")
def get_scheduler_status():
    """获取调度器状态"""
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
        })
    return {
        "scheduler_running": scheduler.running,
        "jobs": jobs,
    }
