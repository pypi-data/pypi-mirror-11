from datetime import datetime

from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, CHAR, DateTime, String, ForeignKey, PrimaryKeyConstraint, Unicode, and_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound

db = SQLAlchemy()


class Agent(db.Model):
    __tablename__ = 'agents'

    uuid = Column('uuid', CHAR(36), primary_key=True, nullable=False)
    name = Column('name', Unicode, nullable=False)
    last_seen = Column('last_seen', DateTime, default=datetime.utcnow)

    @staticmethod
    def get_agent(agent_uuid, agent_name):
        """
        Get existing Agent instance from DB or insert a new one if none exists.

        :param agent_uuid: Agent identifier
        :param agent_name: Agent name to use when creating new instance
        :return: Agent instance
        """
        try:
            agent = db.session.query(Agent).filter(Agent.uuid == agent_uuid).one()
        except NoResultFound:
            current_app.logger.debug('Registering new agent {0}'.format(agent_uuid))
            agent = Agent(uuid=agent_uuid, name=agent_name)
            db.session.add(agent)
        return agent

    def update_capabilities(self, agent_capabilities):
        """
        Update capabilities of the agent to match the new definitions in agent_capabilities

        :param agent_capabilities: A dict describing the new capability set
        """

        # format capabilities list as a dict of (name,version) pairs
        new_capabilities = {name: int(info['version']) for name, info in agent_capabilities.items()}

        # Update existing capabilities
        for capability in self.capabilities:
            if capability.type in new_capabilities:
                capability.version = new_capabilities[capability.type]
                del new_capabilities[capability.type]
            else:
                self.capabilities.remove(capability)

        # Add new capabilities
        for name, version in new_capabilities.items():
            self.capabilities.append(
                AgentCapability(
                    type=name,
                    version=version
                )
            )


class AgentCapability(db.Model):
    __tablename__ = 'agent_capabilities'

    agent_uuid = Column('agent_uuid', CHAR(36), ForeignKey('agents.uuid'))
    agent = relationship(Agent, backref=backref("capabilities", cascade="all, delete-orphan"))

    type = Column('type', String)
    version = Column('version', Integer)

    __table_args__ = (PrimaryKeyConstraint(agent_uuid, type, version),)


class Task(db.Model):
    __tablename__ = 'tasks'

    uuid = Column('uuid', CHAR(36), primary_key=True)
    test_id = Column('test_id', CHAR(36), nullable=False)
    type = Column('type', String)
    version = Column('version', Integer)

    # Data that goes to agent with the task
    data = Column('data', String)  # TODO - use json blob with psql
    # Data that was returned from agent
    result_data = Column('result_data', String)  # TODO - use json blob with psql

    # Agent that has been assigned to take care of the task - NULL if not claimed yet
    assigned_agent_uuid = Column('assigned_agent_uuid', CHAR(36), ForeignKey('agents.uuid'))
    assigned_agent = relationship(Agent, backref="tasks")

    # When was the task added
    created = Column('created', DateTime, default=datetime.utcnow, nullable=False)
    # When was the task claimed by agent - NULL if not claimed yet
    claimed = Column('claimed', DateTime, nullable=True)
    # When was the task completed by agent - NULL if not completed yet
    completed = Column('completed', DateTime, nullable=True)
    # When did the task fail - NULL if hasn't failed yet, additional info in error-field
    failed = Column('started', DateTime, nullable=True)
    # Error message that should only be present if failed is set
    error = Column('error', Unicode, nullable=True)

    @staticmethod
    def claim_tasks(agent, max_tasks):
        """
        Claim tasks to be handled by an agent.

        :param agent: The agent to assign tasks to
        :param max_tasks: Maximum number of tasks to assign
        :return: A generator enumerating assigned tasks
        """
        query = db.session.query(AgentCapability, Task).filter(Task.assigned_agent_uuid.is_(None)). \
            filter(AgentCapability.agent_uuid == agent.uuid). \
            filter(and_(AgentCapability.type == Task.type, AgentCapability.version == Task.version))

        # Assign available tasks to the agent and mark them as being in process
        for _, task in query[0:max_tasks]:
            current_app.logger.info("Claiming task {} for agent {}".format(task.uuid, agent.uuid))
            task.assigned_agent_uuid = agent.uuid
            task.claimed = datetime.utcnow()
            yield task
