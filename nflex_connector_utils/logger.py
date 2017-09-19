class Logger():
    """ Nflex Logger is simple wrapper for context.log which is
        supposed to be used in nflex module.
        This logger is achieves the following:

        - Each log message has header including customer_id, account_id, resource_id
          (optional).
        - The output destination can be changed easily between context.log and print
        - When you execute via flexer or GUI for test, you need to use "print" so you
          can see log from the result of flexer api(GUI used this api implicitly) you
          need to use "context.log" so you can see log at module status page. Through
          the context.module_id we dynamically know when it should use the logs
          API as this parameter is only set on production environments.

        Args:

            context (dict): nflex module's context
            customer_id (str): event's customer id
            account_id (str): event's account id
            resource_id (str): event's resource id (nullable)

        Examples:
            Set up logger::

                # Nflex Module Context
                context= {}

                # Nflex
                event = {
                    'customer_id': 'fake-id',
                    'account_id': 'fake-id',
                    'resource': {
                        'id': 'fake-resource-id'
                    }
                }

                logger = Logger(
                    context,
                    customer_id=event.get('customer_id', ''),
                    account_id=event.get('account_id', ''),
                    resource_id=event['resource']['id']
                )

            Log information with severity info, warn or error::

                logger.info('logging info %s' % ('something'))
                logger.warn('logging warn %s' % ('something'))
                logger.error('logging error %s' % ('something'))

    """  # noqa
    def __init__(self, context, customer_id, account_id, resource_id=None):
        self.context = context
        self.customer_id = customer_id
        self.account_id = account_id
        self.resource_id = resource_id
        self.template = "Target(customer: {customer_id},"\
            "account: {account_id}, resource: {resource_id}): {body}"

        severities = ['info', 'warn', 'error', 'exception']
        from functools import partial
        for severity in severities:
            setattr(self, severity, partial(self._log, severity))

    def _log(self, severity, body):
        prettied = self.template.format(
            customer_id=self.customer_id,
            account_id=self.account_id,
            resource_id=self.resource_id,
            body=body
            )
        if self.context.module_id:
            self.context.log(prettied, severity)
        else:
            print(severity + '\t' + prettied)
